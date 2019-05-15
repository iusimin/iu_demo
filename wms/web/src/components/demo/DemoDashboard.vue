<template>
  <div>
    <active-sort-job v-model="active_job_id"></active-sort-job>
    <v-container fluid grid-list-md>
      <snackbar ref="Snackbar"></snackbar>
      <v-layout row wrap>
        <v-flex md2>
          <v-btn color="tertiary" @click="cancelParcels">取消数据库所有包裹</v-btn>
        </v-flex>
        <v-flex md2>
          <v-layout row wrap>
            <v-flex md4>
              <v-text-field v-model="parcel_count" label="包裹数量" placeholder="包裹数量"></v-text-field>
            </v-flex>
            <v-flex md8>
              <v-btn color="primary" @click="createParcels">创建包裹</v-btn>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-flex md2>
          <v-btn color="secondary" @click="inboundAllParcels">扫描入库所有包裹</v-btn>
        </v-flex>
        <v-flex md2>
          <v-btn color="info" @click="setReadyToShip">设置所有包裹为可出库</v-btn>
        </v-flex>
        <v-flex md2>
          <v-btn color="warning" @click="getActiveParcels">刷新包裹列表</v-btn>
        </v-flex>
        <v-flex md2>
          <v-btn color="accent" @click="runSortJob">跑分拣任务</v-btn>
        </v-flex>
        <v-flex md12>
          <v-data-table
            :headers="active_parcels.headers"
            :items="active_parcels.parcels"
            :loading="active_parcels.loading"
            :pagination.sync="active_parcels.pagination"
            :total-items="active_parcels.total_count"
            :rows-per-page-items="[20, 30, 50, 100]"
          >
            <template slot="headerCell" slot-scope="{ header }">
              <span class="font-weight-light text-warning text--darken-3" v-text="header.text"/>
            </template>
            <template slot="items" slot-scope="{ index, item }">
              <td>{{ index + 1 }}</td>
              <td>{{ item.tracking_id }}</td>
              <td>{{ item.status_text }}</td>
              <td>{{ item.weight }}</td>
              <td>{{ item.timeline.inbound }}</td>
              <td>{{ item.ready_to_ship }}</td>
            </template>
          </v-data-table>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import Snackbar from "@/components/common/Snackbar.vue";
import ActiveSortJob from "@/components/sorter/ActiveSortJob.vue";
export default {
  data: () => ({
    active_job_id: null,
    parcel_count: 20,
    active_parcels: {
      headers: [
        { text: "序号", sortable: false },
        { text: "Tracking Id", sortable: false, value: "tracking_id" },
        { text: "状态", sortable: false, value: "status_text" },
        { text: "重量", sortable: false, value: "weight" },
        { text: "入库时间", sortable: false },
        { text: "是否可出库", sortable: false }
      ],
      parcels: [],
      loading: true,
      pagination: {
        descending: false
      },
      total_count: 10
    }
  }),
  components: {
    Snackbar,
    ActiveSortJob
  },
  mounted: function() {
    var vm = this;
    vm.getActiveParcels();
  },
  computed: {},
  methods: {
    cancelParcels: function() {
      var vm = this;
      vm.api
        .demoCancelAllParcels()
        .then(resp => {
          vm.getActiveParcels();
          alert("Success");
        })
        .catch(resp => {
          alert("Failed");
        });
    },
    createParcels: function() {
      var vm = this;
      vm.api
        .demoCreateInboundParcels(vm.parcel_count)
        .then(resp => {
          vm.getActiveParcels();
          alert("Success");
        })
        .catch(resp => {
          alert("Failed");
        });
    },
    inboundAllParcels: function() {
      var vm = this;
      vm.api
        .demoInboundAllParcels()
        .then(resp => {
          vm.getActiveParcels();
          alert("Success");
        })
        .catch(resp => {
          alert("Failed");
        });
    },
    setReadyToShip: function() {
      var vm = this;
      vm.api
        .demoSetReadyToShip()
        .then(resp => {
          vm.getActiveParcels();
          alert("Success");
        })
        .catch(resp => {
          alert("Failed");
        });
    },
    getActiveParcels: function() {
      var vm = this;
      vm.api
        .demoGetUncancelledParcels(vm.active_parcels.pagination)
        .then(resp => {
          vm.active_parcels.parcels = resp.data;
          vm.active_parcels.total_count = resp.total_count;
        })
        .catch(resp => {
          alert("0");
        });
    },
    runSortJob: function() {
      var vm = this;
      vm.api
        .demoRunSortJob(vm.active_job_id)
        .then(resp => {
          alert("Success");
        })
        .catch(resp => {
          alert(resp.description);
        });
    }
  }
};
</script>

<style lang="scss">
</style>
