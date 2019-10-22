# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime
from itertools import groupby

from bson import ObjectId

from wms.lib.combine_parcel.data_accessor.inbound_parcel_accessor import \
    CPInboundParcelAccessor
from wms.lib.combine_parcel.data_accessor.sort_job_accessor import \
    SortJobAccessor
from wms.model.mongo.combine_parcel.combine_pool import (CPSortAllocateGroupId,
                                                         CPSortPool)
from wms.model.mongo.combine_parcel.inbound_parcel import CPInboundParcel
from wms.model.mongo.combine_parcel.sort_job import CPSortJob
from wms.model.mongo.warehouse import Warehouse


class SortJobUtil(object):

    @classmethod
    def check_inbound_parcel_ready_to_ship(cls, job_id):
        job_accessor = SortJobAccessor(job_id)
        job_accessor.check_job_type(CPSortJob.Type.CheckInboundParcelReadyToShip)
        job_accessor.start_calculation()
        job_accessor.flush()

        job = job_accessor.sort_job

        try:
            inbound_parcels = CPInboundParcel.find_iter({
                "warehouse_id": job.warehouse_id,
                "status": CPInboundParcel.Status.Inbound,
                "ready_to_ship": False
            })

            parcel_groups = defaultdict(list)
            for parcel in inbound_parcels:
                parcel_groups[parcel.combine_id].append(parcel)

            combine_ids = list(parcel_groups.keys())
            if combine_ids:
                utc_now = datetime.utcnow()
                all_parcels = CPInboundParcel.find_iter({
                    "combine_id": {
                        "$in": combine_ids
                    }
                })
                all_parcel_groups = defaultdict(list)
                for parcel in all_parcels:
                    all_parcel_groups[parcel.combine_id].append(parcel)

                ready_to_ship_parcels = defaultdict(list)
                for combine_id, parcels in parcel_groups.items():
                    all_combine_id_parcels = all_parcel_groups[combine_id]
                    if len([parcel for parcel in all_combine_id_parcels if not parcel.ready_to_ship]) == len(parcels):
                        ready_to_ship_parcels[combine_id] = parcels
                    else:
                        for parcel in parcels:
                            if parcel.latest_ship_datetime < utc_now:
                                ready_to_ship_parcels[combine_id].append(parcel)

                if ready_to_ship_parcels:
                    ready_to_ship_tracking_ids = []
                    for parcels in ready_to_ship_parcels.values():
                        for parcel in parcels:
                            ready_to_ship_tracking_ids.append(parcel.tracking_id)
                    if ready_to_ship_tracking_ids:
                        CPInboundParcelAccessor.bulk_set_ready_to_ship(ready_to_ship_tracking_ids)

            job_accessor.success()
        except Exception as ex:
            job_accessor.fail(str(ex))
        finally:
            job_accessor.flush()

    @classmethod
    def allocate_cabinet_for_parcels(cls, job_id):
        job_accessor = SortJobAccessor(job_id)
        job_accessor.check_job_type(CPSortJob.Type.AllocateCabinetLattice)
        job_accessor.start_calculation()
        job_accessor.flush()

        job = job_accessor.sort_job

        try:
            warehouse = Warehouse.by_warehouse_id(job.warehouse_id)
            inbound_parcels = CPInboundParcel.find_iter({
                "warehouse_id": job.warehouse_id,
                "status": CPInboundParcel.Status.Inbound,
                "ready_to_ship": True
            })

            parcel_groups = defaultdict(list)
            for parcel in inbound_parcels:
                parcel_groups[parcel.combine_id].append(parcel)

            combine_ids = parcel_groups.keys()
            if combine_ids:
                group_ids = CPSortAllocateGroupId.allocate(
                    len(combine_ids), warehouse.sort_batch_size)
                group_dict = dict(zip(combine_ids, group_ids))

                lattice_id = 1
                cabinet_id = str(ObjectId())
                for combine_id, parcels in parcel_groups.items():
                    group_length = len(parcels)
                    sort_type = CPSortPool.SortType.DirectShip if group_length == 1 else CPSortPool.SortType.Combined
                    for parcel in parcels:
                        group_id = group_dict[combine_id]
                        CPSortPool.create(
                            job_id=job_id,
                            tracking_id=parcel.tracking_id,
                            sort_type=sort_type,
                            group_ids=group_id,
                            cabinet_id=cabinet_id,
                            lattice_id=lattice_id
                        )
                    lattice_id += 1

            job_accessor.success()
        except Exception as ex:
            job_accessor.fail(str(ex))
        finally:
            job_accessor.flush()

    @classmethod
    def get_parcel_sort_info(cls, job_id, tracking_id, round_id):
        parcel = CPSortPool.by_tracking_id(job_id, tracking_id)

        if not parcel:
            raise ValueError("Parcel with tracking id {0} didn't exist in job {1}.".format(
                tracking_id, job_id))

        info_dict = parcel.to_dict()
        info_dict["group_ids_string"] = parcel.group_ids_string
        info_dict["round_group_id"] = parcel.get_group_id_by_round(round_id - 1)
        return info_dict

    @classmethod
    def get_combine_cabinet_from_first_tracking_id(cls, job_id, tracking_id):
        job_accessor = SortJobAccessor(job_id)
        parcel = CPSortPool.by_tracking_id(job_id, tracking_id)

        if not parcel:
            raise ValueError("Parcel with tracking id {0} didn't exist in job {1}.".format(
                tracking_id, job_id))

        parcels = CPSortPool.find({
            "job_id": job_id,
            "cabinet_id": parcel.cabinet_id
        })

        tracking_ids = [parcel.tracking_id for parcel in parcels]
        inbound_parcels = CPInboundParcel.by_tracking_ids(tracking_ids)
        inbound_parcel_dict = {
            parcel.tracking_id: parcel for parcel in inbound_parcels}

        parcels = [parcel.to_dict() for parcel in parcels]
        def key_func(x): return x["lattice_id"]
        parcels = sorted(parcels, key=key_func)
        parcel_groups = groupby(parcels, key=key_func)

        res = []
        for group in parcel_groups:
            lattice_id = group[0]
            parcels_in_lattice = list(group[1])
            for parcel in parcels_in_lattice:
                tracking_id = parcel["tracking_id"]
                inbound_parcel = inbound_parcel_dict[tracking_id]
                parcel["inbound_weight"] = inbound_parcel.weight
                parcel["inbound_datetime"] = inbound_parcel.timeline.inbound.strftime(
                    "%Y-%m-%d %H:%M:%S")
                parcel["lattice_id"] = lattice_id

            res.append(parcels_in_lattice)

        return job_accessor.sort_job, res
