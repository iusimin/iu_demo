<template>
  <div>
    <v-container fill-height fluid grid-list-xl>
      <v-layout wrap>
        <v-flex sm6 xs12 md6 lg4>
          <material-operation-card
            color="green"
            icon="mdi-store"
            title="入库安检"
            value="安检，区分普通货物、特殊货物、超规特货等"
            sub-icon="mdi-calendar"
            sub-text="Last 24 Hours"
            click-link="/inbound-scan"
          />
        </v-flex>
        <v-flex sm6 xs12 md6 lg4>
          <material-operation-card
            color="orange"
            icon="mdi-content-copy"
            title="分拣"
            value="1-3轮分拣库内包裹"
            sub-icon="mdi-alert"
            sub-text="Get More Space..."
            click-link="/sorter"
          />
        </v-flex>
        <v-flex sm6 xs12 md6 lg4>
          <material-operation-card
            color="red"
            icon="mdi-information-outline"
            title="播种并打单"
            value="分拣完成后以筐为单位执行"
            sub-icon="mdi-tag"
            sub-text="Tracked from Github"
            click-link="/seed"
          />
        </v-flex>

        <v-flex sm6 xs12 md6 lg4>
          <material-operation-card
            color="accent"
            icon="mdi-atom"
            title="直发打单"
            value="分拣结果为‘直接发送’的包裹执行直发打单"
            sub-icon="mdi-calendar"
            sub-text="Last 24 Hours"
            click-link="/directship"
          />
        </v-flex>
        <v-flex sm6 xs12 md6 lg4>
          <material-operation-card
            color="info"
            icon="mdi-autorenew"
            title="出库扫描"
            value="打印并贴好后程面单"
            sub-icon="mdi-alert"
            sub-text="Get More Space..."
            click-link="/outboundscan"
          />
        </v-flex>
        <v-flex sm6 xs12 md6 lg4>
          <material-operation-card
            color="warning"
            icon="mdi-azure"
            title="查询与报表"
            value="综合查询功能"
            sub-icon="mdi-tag"
            sub-text="Tracked from Github"
          />
        </v-flex>
        <v-flex md12 lg6>
          <material-card color="orange" title="分拣任务" text="分拣任务列表">
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
          </material-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "HomeContent",
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
  props: [],
  components: {},
  computed: {},
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
