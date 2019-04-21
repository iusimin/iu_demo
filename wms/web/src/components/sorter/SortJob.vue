<template>
  <v-container fluid>
    <v-layout>
      <!-- <v-flex md12 lg12>
          <v-btn>新建分拣任务</v-btn>
      </v-flex> -->
      <v-flex md12>
        <v-data-table
          :headers="sort_job_info.headers"
          :items="sort_job_info.jobs"
          :loading="sort_job_info.loading"
          hide-actions
          :pagination.sync="sort_job_info.pagination"
          :total-items="sort_job_info.total_count"
        >
          <template slot="headerCell" slot-scope="{ header }">
            <span class="font-weight-light text-warning text--darken-3" v-text="header.text"/>
          </template>
          <template slot="items" slot-scope="{ index, item }">
            <td>{{ index + 1 }}</td>
            <td>{{ item.job_id }}</td>
            <td class="text-xs-right">{{ item.status_text }}</td>
            <td class="text-xs-right">{{ item.job_finish_datetime }}</td>
            <td class="text-xs-right">{{ item.parcel_count }}</td>
          </template>
        </v-data-table>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    sort_job_info: {
      headers: [
        {
          text: "序号",
          align: "left",
          sortable: false
        },
        {
          text: "任务ID",
          align: "left",
          sortable: false,
          value: "job_id"
        },
        { text: "状态", align: "right", sortable: false, value: "status_text" },
        {
          text: "时间",
          align: "right",
          sortable: true,
          value: "job_finish_datetime"
        },
        {
          text: "包裹数量",
          align: "right",
          sortable: false,
          value: "parcel_count"
        }
      ],
      jobs: [],
      loading: true,
      pagination: {},
      total_count: 10
    }
  }),
  components: {},
  mounted: function() {
    var vm = this;
    vm.getSortJobs();
  },
  methods: {
    getSortJobs: function() {
      var vm = this;
      vm.api.getSortJobs(
        vm.sort_job_info.pagination,
        resp => {
          vm.sort_job_info.jobs = resp.data;
          vm.sort_job_info.total_count = resp.total_count;
        },
        resp => {
          alert("0");
        }
      );
    }
  },
  watch: {
    "sort_job_info.pagination": {
      handler: function(newVal, oldVal) {
        var vm = this;
        vm.getSortJobs();
      },
      deep: true
    }
  }
};
</script>

<style lang="scss">
</style>
