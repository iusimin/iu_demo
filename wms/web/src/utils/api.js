import noty from "noty";
import axios from "axios";

var _axios_call = function (config, loader) {
    if (loader) loader.show();
    return new Promise((resolve, reject) => {
        axios(config)
            .then(function (resp) {
                if (loader) loader.hide();
                if (resolve) resolve(resp.data);
            })
            .catch(function (error) {
                if (loader) loader.hide();
                if (error.response) {
                    if (reject) {
                        reject(error.response.data);
                    } else {
                        new noty({
                            text: error.response.data.msg,
                            type: "error"
                        }).show();
                        //log.error(error.response.data)
                    }
                } else {
                    console.log(error);
                    //log.error(error)
                }
            });
    });
};

export default {
    buildQueryString: function (param_dict) {
        var esc = encodeURIComponent;
        return Object.keys(param_dict)
            .map(k => esc(k) + '=' + esc(param_dict[k]))
            .join('&');
    },
    call: function (method, url, query, params, loader) {
        var data = params;
        /* _.pickBy(params, e => {
                   return !_.isNil(e)
               }); */
        //var xsrf_token = $("#xsrf-container").find("input").val();
        url = 'api/' + url;
        if (query) {
            url = url + "?" + this.buildQueryString(query)
        }
        var config = {
            data: data,
            method: method,
            url: url,
            headers: {
                //'X-XSRFToken': xsrf_token
            }
        };
        return _axios_call(config, loader);
    },
    login: function (username, password, remember_me) {
        return this.call(
            "post",
            "login",
            null, {
                username: username,
                password: password
            }
        );
    },
    checkLogin: function () {
        return this.call("get", "login", null, null);
    },
    getOperatorWarehouse: function () {
        return this.call("get", "operator-warehouse", null, null);
    },
    updateOperatorWarehouseSetting: function (warehouse_id, setting) {
        return this.call("put", "operator-warehouse", null, {
            warehouse_id: warehouse_id,
            ...setting
        });
    },
    inboundParcel: function (tracking_id, parcel) {
        return this.call("post", "inbound-parcel/" + tracking_id + ":inbound", null, parcel);
    },
    getInboundParcelDetail: function (tracking_id) {
        return this.call("get", "inbound-parcel/" + tracking_id, null, null);
    },
    getParcelSortInfo: function (tracking_id, job_id, round_id) {
        return this.call(
            "get",
            "sort-info", {
                tracking_id: tracking_id,
                job_id: job_id,
                round_id: round_id
            },
            null
        );
    },
    getSeedCabinet: function (tracking_id, job_id) {
        return this.call(
            "get",
            "seed-pool", {
                tracking_id: tracking_id,
                job_id: job_id
            },
            null
        );
    },
    getSortJobs: function (job_type, pagination) {
        return this.call(
            "post", // post as get
            "sort-jobs", 
            null, {
                "query": {
                    "job_type": job_type
                },
                pagination: pagination
            }
        );
    },
    createNewSortJob: function (job_type) {
        return this.call(
            "post",
            "sort-job",
            null, {
                job_type: job_type
            }
        );
    },
    getSortJobDetail: function (job_id) {
        return this.call(
            "get",
            "sort-job", {
                job_id: job_id
            },
            null
        );
    },
    cancelSortJob: function (job_id) {
        return this.call(
            "put",
            "sort-job",
            null, {
                job_id: job_id,
                action: "Cancel"
            }
        );
    },
    getActiveSortJob: function () {
        return this.call("get", "active-sort-job", null, null);
    },
    submitDirectShip: function (tracking_id, parcel) {
        return this.call("put", "inbound-parcel/" + tracking_id + ":directship", null, parcel);
    },
    getCombinedLogisticsOrder: function (job_id, weight, tracking_ids) {
        return this.call("post", "inbound-parcels:combine", null, {
            job_id: job_id,
            weight: weight,
            tracking_ids: tracking_ids
        });
    },

    //For demo only.
    demoCancelAllParcels: function () {
        return this.call("post", "demo:cancel_all_parcels", null, {});
    },
    demoCreateInboundParcels: function (count) {
        return this.call("post", "demo:create_parcels", null, {
            count: count
        });
    },
    demoInboundAllParcels: function () {
        return this.call("post", "demo:inbound_all_parcels", null, {});
    },
    demoSetReadyToShip: function () {
        return this.call("post", "demo:set_ready_to_ship", null, {});
    },
    demoGetUncancelledParcels: function (pagination) {
        return this.call("post", "demo/uncancelled-parcels", null, {
            pagination: pagination
        });
    },
    demoRunSortJob: function (job_id) {
        return this.call("post", "demo:run_sort_job", null, {
            job_id: job_id
        });
    }
};