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
              <!-- <v-flex md6>进度 {{ seeded_parcels.length }} / {{ all_parcels.length }}</v-flex> -->
            </v-layout>
          </v-card-title>
          <v-card-title class="error" v-else>
            <v-layout>
              <v-flex md12>不属于当前上架的批次</v-flex>
            </v-layout>
          </v-card-title>
        </v-card>
        <v-card>
          <v-card-text>
            <div class="font-weight-medium headline">{{ current_tracking_id }}</div>
            <div>分拣结果: {{ current_parcel ? current_parcel.lattice_id : null }}</div>
            <div>入库重量: {{ current_parcel ? current_parcel.inbound_weight : null }}</div>
            <div>入库时间: {{ current_parcel ? current_parcel.inbound_datetime : null }}</div>
          </v-card-text>
        </v-card>
        <v-card>
          <v-layout>
            <v-flex md6>
              <v-card>
                <div>
                  <span>未上架</span>
                  <v-chip class="text-xs-right" color="indigo" text-color="white">
                    {{ pending_table.data.length }}
                  </v-chip>
                </div>
              </v-card>
              <v-data-table
                :headers="pending_table.headers"
                :items="pending_table.data"
                hide-actions
                hide-headers
                class="elevation-1"
                no-data-text=""
              >
                <template v-slot:items="props">
                  <td style="padding:3px;height:30px;">{{ props.item.tracking_id }}</td>
                </template>
              </v-data-table>
            </v-flex>
            <v-flex md6>
              <v-card>
                <div>
                  <span>已上架</span>
                  <v-chip class="text-xs-right" color="indigo" text-color="white">
                    {{ seeded_table.data.length }}
                  </v-chip>
                </div>
              </v-card>
              <v-data-table
                :headers="seeded_table.headers"
                :items="seeded_table.data"
                hide-actions
                hide-headers
                class="elevation-1"
                no-data-text=""
              >
                <template v-slot:items="props">
                  <td style="padding:3px;height:30px;" class="text-xs-right">{{ props.item.tracking_id }}</td>
                </template>
              </v-data-table>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
      <v-flex md9>
        <cabinet ref="Cabinet" :parcels="null" :size_x="10" :size_y="5"></cabinet>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Cabinet from "../../components/outbound/Cabinet";
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
    vm.pending_table.data = vm.all_parcels;
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
    seeded_parcels: function() {
      var vm = this;
      return vm.seeded_table.data;
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
      vm.tracking_id_updated();
    },
    reset_cabinet: function() {
      var vm = this;
      vm.$refs.Cabinet.reset(vm.target_parcels);
    },
    tracking_id_updated: function() {
      var vm = this;
      var parcel = vm.parcels_by_tracking_id[vm.current_tracking_id];
      if (vm.current_tracking_id && !parcel) {
        vm.parcel_valid = false;
      } else {
        vm.parcel_valid = true;
      }
      if (parcel) {
        vm.$refs.Cabinet.seed_parcel(parcel);
      }
      vm.adjust_table();
    },
    adjust_table: function() {
      var vm = this;
      if (vm.current_tracking_id) {
        vm.pending_table.data = vm.pending_table.data.filter(function(ele) {
          return ele.tracking_id != vm.current_tracking_id;
        });
        //vm.seeded_table.data
        if (
          vm.seeded_table.data.findIndex(
            ele => ele.tracking_id === vm.current_tracking_id
          ) === -1
        ) {
          vm.seeded_table.data.unshift(vm.current_parcel);
        }
      }
    }
  },
  watch: {
    current_tracking_id: {
      handler: function(newValue, oldValue) {
        var vm = this;
        if (newValue) {
          vm.current_tracking_id = newValue;
        }
      },
      deep: true
    }
  }
};
</script>

<style lang="scss">
</style>