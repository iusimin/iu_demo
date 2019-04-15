<template>
  <v-container fluid>
    <v-layout>
      <v-flex md3>
        <div>
          <a style="text-decoration: underline;color:#757575;" @click="toggle_manual">手动输入物流单号</a>
          <v-text-field
            v-if="manual_input"
            v-model="manual_tracking_id"
            @keyup.enter="manual_complete"
            label="物流单号"
          ></v-text-field>
        </div>
        <v-card>
          <v-card-title class="primary" v-if="parcel_valid">
            <v-layout>
              <v-flex md6>当前格子：{{ current_parcel ? current_parcel.lattice_id : null }}</v-flex>
              <!-- <v-flex md6>进度 {{  }} / {{  }}</v-flex> -->
            </v-layout>
          </v-card-title>
          <v-card-title class="error" v-else>
            <v-layout>
              <v-flex md12>不属于当前上架的批次</v-flex>
            </v-layout>
          </v-card-title>
        </v-card>
        <v-card>
          <!-- <v-card-title primary-title>{{ current_tracking_id }}</v-card-title> -->
          <v-card-text>
            <div class="font-weight-medium headline">{{ current_tracking_id }}</div>
            <v-data-table
              :items="current_parcel_info"
              class="elevation-1"
              hide-actions
              hide-headers
            >
              <template v-slot:items="props">
                <td>{{ props.item.name }}</td>
                <td class="text-xs-right">{{ props.item.value }}</td>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
        <v-card>
          <v-card-text>
            <v-layout>
              <v-flex md6>
                <!-- <v-card>
                <div>
                  <span>未上架</span>
                  <span>({{ pending_table.data.length }})</span>
                  <v-chip class="text-xs-right" color="indigo" text-color="white">
                    {{ pending_table.data.length }}
                  </v-chip>
                </div>
                </v-card>-->
                <v-data-table
                  :headers="pending_table.headers"
                  :items="pending_table.data"
                  hide-actions
                  class="elevation-1"
                  no-data-text
                >
                  <template v-slot:items="props">
                    <td>{{ props.item.tracking_id }}</td>
                  </template>
                </v-data-table>
              </v-flex>
              <v-flex md6>
                <!-- <v-card>
                <div>
                  <span>已上架</span>
                  <span>({{ seeded_table.data.length }})</span>
                  <v-chip class="text-xs-right" color="indigo" text-color="white">
                    {{ seeded_table.data.length }}
                  </v-chip>
                </div>
                </v-card>-->
                <v-data-table
                  :headers="seeded_table.headers"
                  :items="seeded_table.data"
                  hide-actions
                  class="elevation-1"
                  no-data-text
                >
                  <template v-slot:items="props">
                    <td class="text-xs-right">{{ props.item.tracking_id }}</td>
                  </template>
                </v-data-table>
              </v-flex>
            </v-layout>
          </v-card-text>
        </v-card>
      </v-flex>
      <v-flex md9>
        <cabinet ref="Cabinet" :parcels="null" :size_x="10" :size_y="5"></cabinet>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-btn color="tertiary" @click="reset_cabinet">清空任务</v-btn>
    </v-layout>
  </v-container>
</template>

<script>
import Cabinet from "@/components/outbound/Cabinet";
import { test_parcels } from "./test_seed_parcels.js";

export default {
  components: {
    Cabinet
  },
  data: () => ({
    pending_table: {
      headers: [
        {
          text: "未上架",
          align: "left",
          sortable: false,
          value: "tracking_id"
        }
      ],
      data: []
    },
    seeded_table: {
      headers: [
        {
          text: "已上架",
          align: "right",
          sortable: false,
          value: "tracking_id"
        }
      ],
      data: []
    },
    current_tracking_id: null,
    parcel_valid: true,
    manual_input: false,
    manual_tracking_id: null,
    cabinet_size: [8, 6],
    target_parcels: test_parcels
  }),
  mounted: function() {
    var vm = this;
    vm.reset_cabinet();
  },
  computed: {
    all_parcels: function() {
      var vm = this;
      var res = [];
      vm.target_parcels.forEach(function(parcels) {
        parcels.forEach(function(parcel) {
          res.push(parcel);
        });
      });
      return res;
    },
    parcels_by_tracking_id: function() {
      var vm = this;
      var res = {};
      vm.target_parcels.forEach(function(parcels) {
        parcels.forEach(function(parcel) {
          res[parcel.tracking_id] = parcel;
        });
      });
      return res;
    },
    current_parcel: function() {
      var vm = this;
      var parcel = null;
      if (vm.current_tracking_id) {
        parcel = vm.parcels_by_tracking_id[vm.current_tracking_id];
      }
      return parcel;
    },
    current_parcel_info: function() {
      var vm = this;
      return [
        {
          name: "分拣结果",
          value: vm.current_parcel ? vm.current_parcel.lattice_id : null
        },
        {
          name: "入库重量",
          value: vm.current_parcel ? vm.current_parcel.inbound_weight : null
        },
        {
          name: "入库时间",
          value: vm.current_parcel ? vm.current_parcel.inbound_datetime : null
        }
      ];
    },
    current_lattice: function() {
      var vm = this;
      var lattice = null;
      if (vm.current_tracking_id) {
        var lattice_id = vm.current_parcel.lattice_id;
        lattice = vm.target_parcels[lattice_id - 1];
      }
      return lattice;
    }
  },
  methods: {
    toggle_manual: function() {
      var vm = this;
      vm.manual_input = !vm.manual_input;
      vm.manual_tracking_id = null;
    },
    manual_complete: function() {
      var vm = this;
      vm.manual_input = false;
      vm.current_tracking_id = vm.manual_tracking_id;
    },
    reset_cabinet: function() {
      var vm = this;
      vm.target_parcels.forEach(function(lattice) {
        lattice.forEach(function(ele) {
          ele.seeded = false;
        });
      });
      vm.current_tracking_id = null;
      vm.$refs.Cabinet.reset(vm.target_parcels);
    },
    tracking_id_updated: function() {
      var vm = this;
      if (vm.current_tracking_id && !vm.current_parcel) {
        vm.parcel_valid = false;
      } else {
        vm.parcel_valid = true;
      }
      if (vm.current_parcel) {
        vm.$refs.Cabinet.seed_parcel(vm.current_parcel);
        vm.current_parcel.seeded = true;
      }
      vm.adjust_table();
    },
    adjust_table: function() {
      var vm = this;
      vm.pending_table.data = [];
      vm.seeded_table.data = [];
      if (vm.current_lattice) {
        console.log("11");
        vm.pending_table.data = vm.current_lattice.filter(function(ele) {
          return !ele.seeded;
        });
        vm.seeded_table.data = vm.current_lattice.filter(function(ele) {
          return ele.seeded;
        });
      }
    }
  },
  watch: {
    current_tracking_id: {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.tracking_id_updated();
      },
      deep: true
    }
  }
};
</script>

<style lang="scss">
</style>
