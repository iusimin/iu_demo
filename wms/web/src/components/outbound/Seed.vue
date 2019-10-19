<template>
  <v-container fluid>
    <snackbar ref="Snackbar"></snackbar>
    <v-layout>
      <v-flex md3>
        <div>
          <a style="text-decoration: underline;color:#757575;" @click="toggle_manual">手动输入物流单号</a>
          <v-text-field
            class="stop-propagation"
            v-if="manual_input"
            v-model="manual_tracking_id"
            @keyup.enter="manual_complete"
            label="物流单号"
          ></v-text-field>
        </div>
        <v-card>
          <v-card-title class="primary" v-if="tracking_id_valid">
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
        <cabinet
          ref="Cabinet"
          :parcels="null"
          :size_x="cabinet_size.width"
          :size_y="cabinet_size.height"
        ></cabinet>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-btn color="tertiary" @click="reset_cabinet">清空任务</v-btn>
    </v-layout>
    <v-layout row justify-center>
      <v-dialog v-model="show_weight_dialog" persistent max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">合并包裹重量</span>
          </v-card-title>
          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12 sm6 md4>
                  <v-text-field label="合并包裹重量" v-model="combined_weight" required></v-text-field>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" flat @click="submitCombinedWeight">提交</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
  </v-container>
</template>

<script>
//TODO antony: refactor later.
import { mapState } from "vuex";
import Cabinet from "@/components/outbound/Cabinet";
import { test_parcels } from "./test_seed_parcels.js";
import ParcelScanListener from "@/components/mixins/ParcelScanListener.vue";
import Snackbar from "@/components/common/Snackbar.vue";
import { printPDF } from "@/utils/print.js";

export default {
  props: ["job_id"],
  components: {
    Cabinet,
    Snackbar
  },
  mixins: [ParcelScanListener],
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
    tracking_id_valid: true,
    manual_input: false,
    manual_tracking_id: null,
    cabinet_size: {
      // TODO antony: Initialized from warehouse setting
      width: 0,
      height: 0
    },
    target_parcels: [],
    show_weight_dialog: false,
    combined_weight: null,
    logistics_order: null
  }),
  mounted: function() {
    var vm = this;
    vm.initWarehouseCabinetSize();
  },
  computed: {
    ...mapState(["seed_mode"]),
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
      if (vm.current_tracking_id && vm.current_parcel) {
        var lattice_id = vm.current_parcel.lattice_id;
        lattice = vm.target_parcels[lattice_id - 1];
      }
      return lattice;
    }
  },
  methods: {
    stopInputPropagation: function(e) {
      e.stopPropagation();
    },
    initWarehouseCabinetSize: function() {
      var vm = this;
      vm.api.getOperatorWarehouse().then(resp => {
        vm.cabinet_size = resp.warehouse.cabinet_size;
        vm.$nextTick(function() {
          vm.reset_cabinet();
        });
      });
    },
    toggle_manual: function() {
      var vm = this;
      vm.manual_input = !vm.manual_input;
      vm.manual_tracking_id = null;
      vm.$nextTick(function() {
        var eles = document.getElementsByClassName("stop-propagation");
        for (let i = 0; i < eles.length; i++) {
          eles[i].addEventListener("keyup", vm.stopInputPropagation);
        }
      });
    },
    manual_complete: function() {
      var vm = this;
      vm.manual_input = false;
      vm.current_tracking_id = vm.manual_tracking_id;
    },
    reset_cabinet: function() {
      var vm = this;
      vm.target_parcels = [];
      vm.init_cabinet();
      vm.current_tracking_id = null;
    },
    init_cabinet: function() {
      var vm = this;
      vm.target_parcels.forEach(function(lattice) {
        lattice.forEach(function(ele) {
          ele.seeded = false;
          ele.combine_scanned = false;
        });
      });
      vm.$refs.Cabinet.reset(vm.target_parcels);
    },
    tracking_id_updated: function() {
      var vm = this;
      if (vm.seed_mode == 0) {
        if (vm.target_parcels.length == 0) {
          vm.init_target_parcels(vm.seed_tracking_id);
        } else {
          vm.seed_tracking_id();
        }
      } else if (vm.seed_mode == 1) {
        vm.combineScanParcel();
      }
    },
    seed_tracking_id: function() {
      var vm = this;
      var current_parcel = vm.parcels_by_tracking_id[vm.current_tracking_id];
      if (vm.current_tracking_id && !current_parcel) {
        vm.tracking_id_valid = false;
      } else {
        vm.tracking_id_valid = true;
      }
      if (current_parcel) {
        vm.$refs.Cabinet.seed_parcel(current_parcel);
        current_parcel.seeded = true;
      }
      vm.adjust_table();
    },
    init_target_parcels: function(cb) {
      var vm = this;
      if (vm.target_parcels.length == 0) {
        vm.api
          .getSeedCabinet(vm.current_tracking_id, vm.job_id)
          .then(resp => {
            vm.cabinet_size = resp.job.warehouse_seed_cabinet_size;
            vm.target_parcels = resp.parcels;
            vm.$nextTick(function() {
              vm.init_cabinet();
              vm.$nextTick(cb);
            });
          })
          .catch(resp => {
            alert("error");
          });
      }
    },
    adjust_table: function() {
      var vm = this;
      vm.pending_table.data = [];
      vm.seeded_table.data = [];
      if (vm.current_lattice) {
        vm.pending_table.data = vm.current_lattice.filter(function(ele) {
          return vm.seed_mode == 0 ? !ele.seeded : !ele.combine_scanned;
        });
        vm.seeded_table.data = vm.current_lattice.filter(function(ele) {
          return vm.seed_mode == 0 ? ele.seeded : ele.combine_scanned;
        });
      }
    },
    combineScanParcel: function() {
      var vm = this;
      var current_parcel = vm.parcels_by_tracking_id[vm.current_tracking_id];
      if (current_parcel) {
        vm.$refs.Cabinet.combineScannedParcel(current_parcel);
        current_parcel.combine_scanned = true;
        vm.adjust_table();
        vm.checkLatticeScanComplete(current_parcel);
      }
    },
    checkLatticeScanComplete: function(parcel) {
      var vm = this;
      if (vm.current_lattice) {
        var combine_scanned = vm.current_lattice.filter(function(ele) {
          return ele.combine_scanned;
        });
        if (combine_scanned.length == vm.current_lattice.length) {
          vm.combined_weight = null;
          vm.show_weight_dialog = true;
        }
      }
    },
    submitCombinedWeight: function() {
      var vm = this;
      vm.show_weight_dialog = false;
      if (vm.current_lattice) {
        var combine_scanned_tracking_ids = vm.current_lattice
          .filter(function(ele) {
            return ele.combine_scanned;
          })
          .map(function(ele) {
            return ele.tracking_id;
          });
        vm.api
          .getCombinedLogisticsOrder(
            vm.job_id,
            parseFloat(vm.combined_weight),
            combine_scanned_tracking_ids
          )
          .then(resp => {
            vm.logistics_order = resp.logistics_order;
            printPDF(vm.logistics_order.label_url);
          })
          .catch(resp => {
            vm.$refs.Snackbar.showSnackbar("错误", resp.description, "error");
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
    },
    seed_mode: {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.current_tracking_id = null;
      }
    },
    tracking_id: {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.current_tracking_id = newValue;
      }
    },
    weight: {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.combined_weight = newValue;
        vm.submitCombinedWeight();
      }
    }
  },
  destroyed: function() {
    var vm = this;
    var eles = document.getElementsByClassName("stop-propagation");
    for (let i = 0; i < eles.length; i++) {
      eles[i].removeEventListener("keyup", vm.stopInputPropagation);
    }
  }
};
</script>

<style lang="scss">
</style>
