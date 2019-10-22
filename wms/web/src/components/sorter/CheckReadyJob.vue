<template>
  <v-container fluid grid-list-xl>
    <v-layout wrap>
      <v-flex md12 lg12>
        <v-btn color="primary" @click.stop="show_dialog = true">新建出库判定任务</v-btn>
      </v-flex>
      <v-flex md12 lg12>
        <v-data-table
          :headers="check_job_info.headers"
          :items="check_job_info.jobs"
          :loading="check_job_info.loading"
          :pagination.sync="check_job_info.pagination"
          :total-items="check_job_info.total_count"
          :rows-per-page-items="[20, 30, 50, 100]"
        >
          <template slot="headerCell" slot-scope="{ header }">
            <span class="font-weight-light text-warning text--darken-3" v-text="header.text"/>
          </template>
          <template slot="items" slot-scope="{ index, item }">
            <td>{{ index + 1 }}</td>
            <td>{{ item.job_id }}</td>
            <td class="text-xs-right">{{ item.status_text }}</td>
            <td class="text-xs-right">{{ item.created_datetime }}</td>
            <td class="text-xs-right">
              <div
                v-if="isJobCancelable(item.status)"
                small
                class="mr-2"
                @click="confirmAndcancelCheckJob(item.job_id)"
              >取消任务</div>
            </td>
          </template>
        </v-data-table>
      </v-flex>
      <!-- TODO antony: Refactor -->
      <v-dialog v-model="show_dialog" max-width="290">
        <v-card>
          <v-card-title class="headline">确定创建新的出库判定任务?</v-card-title>
          <v-card-text></v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat="flat" @click="show_dialog = false">取消</v-btn>
            <v-btn color="green darken-1" flat="flat" @click="createNewCheckJob">确定</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="show_cancel_dialog" max-width="290">
        <v-card>
          <v-card-title class="headline">确定取消出库判定任务?</v-card-title>
          <v-card-text></v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat="flat" @click="show_cancel_dialog = false">取消</v-btn>
            <v-btn color="green darken-1" flat="flat" @click="cancelCheckJob">确定</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
  </v-container>
</template>

<script>
import {
  SortJobType
} from "@/constants/constants.js";
export default {
  data: () => ({
    show_dialog: false,
    show_cancel_dialog: false,
    job_to_cancel: null,
    check_job_info: {
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
          text: "创建时间",
          align: "right",
          sortable: true,
          value: "created_datetime"
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
        sortBy: "created_datetime",
        descending: true
      },
      total_count: 10
    }
  }),
  components: {},
  mounted: function() {
    var vm = this;
  },
  methods: {
    getCheckJobs: function() {
      var vm = this;
      vm.api
        .getSortJobs(SortJobType.CheckInboundParcelReadyToShip, vm.check_job_info.pagination)
        .then(resp => {
          vm.check_job_info.jobs = resp.data;
          vm.check_job_info.total_count = resp.total_count;
        })
        .catch(resp => {
          alert("0");
        });
    },
    createNewCheckJob: function() {
      var vm = this;
      vm.show_dialog = false;
      vm.api
        .createNewSortJob(SortJobType.CheckInboundParcelReadyToShip)
        .then(resp => {
          vm.getCheckJobs();
          alert("创建成功！");
        })
        .catch(resp => {
          alert(resp.description);
        });
    },
    confirmAndcancelCheckJob: function(job_id) {
      var vm = this;
      vm.job_to_cancel = job_id;
      vm.show_cancel_dialog = true;
    },
    cancelCheckJob: function() {
      var vm = this;
      vm.show_cancel_dialog = false;
      vm.api
        .cancelSortJob(vm.job_to_cancel)
        .then(resp => {
          vm.getCheckJobs();
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
    "check_job_info.pagination": {
      handler: function(newVal, oldVal) {
        var vm = this;
        vm.getCheckJobs();
      },
      deep: true
    }
  }
};
</script>

<style lang="scss">
</style>
