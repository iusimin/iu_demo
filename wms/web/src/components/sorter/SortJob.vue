<template>
  <v-container fluid grid-list-xl>
    <v-layout wrap>
      <v-flex md12 lg12>
        <v-btn color="primary" @click.stop="show_dialog = true">新建分拣任务</v-btn>
      </v-flex>
      <v-flex md12 lg12>
        <v-data-table
          :headers="sort_job_info.headers"
          :items="sort_job_info.jobs"
          :loading="sort_job_info.loading"
          :pagination.sync="sort_job_info.pagination"
          :total-items="sort_job_info.total_count"
          :rows-per-page-items="[20, 30, 50, 100]"
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
            <td class="text-xs-right">
              <div
                v-if="isJobCancelable(item.status)"
                small
                class="mr-2"
                @click="confirmAndCancelSortJob(item.job_id)"
              >取消任务</div>
            </td>
          </template>
        </v-data-table>
      </v-flex>
      <!-- TODO antony: Refactor -->
      <v-dialog v-model="show_dialog" max-width="290">
        <v-card>
          <v-card-title class="headline">确定创建新的分拣任务?</v-card-title>
          <v-card-text></v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat="flat" @click="show_dialog = false">取消</v-btn>
            <v-btn color="green darken-1" flat="flat" @click="createNewSortJob">确定</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="show_cancel_dialog" max-width="290">
        <v-card>
          <v-card-title class="headline">确定取消分拣任务?</v-card-title>
          <v-card-text></v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat="flat" @click="show_cancel_dialog = false">取消</v-btn>
            <v-btn color="green darken-1" flat="flat" @click="cancelSortJob">确定</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    show_dialog: false,
    show_cancel_dialog: false,
    job_to_cancel: null,
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
        },
        {
          text: "操作",
          align: "right",
          sortable: false
        }
      ],
      jobs: [],
      loading: true,
      pagination: {
        sortBy: "job_finish_datetime",
        descending: true
      },
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
      vm.api
        .getSortJobs(vm.sort_job_info.pagination)
        .then(resp => {
          vm.sort_job_info.jobs = resp.data;
          vm.sort_job_info.total_count = resp.total_count;
        })
        .catch(resp => {
          alert("0");
        });
    },
    createNewSortJob: function() {
      var vm = this;
      vm.show_dialog = false;
      vm.api
        .createNewSortJob(1)
        .then(resp => {
          vm.getSortJobs();
          alert("创建成功！");
        })
        .catch(resp => {
          alert(resp.description);
        });
    },
    confirmAndCancelSortJob: function(job_id) {
      var vm = this;
      vm.job_to_cancel = job_id;
      vm.show_cancel_dialog = true;
    },
    cancelSortJob: function() {
      var vm = this;
      vm.show_cancel_dialog = false;
      vm.api
        .cancelSortJob(vm.job_to_cancel)
        .then(resp => {
          vm.getSortJobs();
          alert("取消成功");
        })
        .catch(resp => {
          alert("取消失败"+resp.description);
        });
    },
    isJobCancelable: function(status) {
      //TODO antony: Use Enum
      return status < 98;
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
