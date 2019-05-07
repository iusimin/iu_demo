<template>
  <v-container fluid grid-list-xl>
    <v-layout wrap>
      <snackbar ref="Snackbar"></snackbar>
      <v-flex md12 lg12>
        <active-sort-job v-model="active_job_id"></active-sort-job>
      </v-flex>
      <v-flex md12 lg12>
        <v-form>
          <v-container>
            <v-layout row wrap>
              <v-flex md12>
                <v-text-field
                  class="stop-propagation"
                  v-model="parcel_scan_info.tracking_id"
                  label="物流单号"
                  required
                ></v-text-field>
              </v-flex>
              <v-flex md12>
                <v-text-field
                  class="stop-propagation"
                  v-model="parcel_scan_info.weight"
                  label="重量"
                  required
                ></v-text-field>
              </v-flex>
              <v-flex offset-md10 md2>
                <v-btn color="success" type="button" @click="submitDirectParcel">打单</v-btn>
              </v-flex>
            </v-layout>
          </v-container>
        </v-form>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import ParcelScanListener from "@/components/mixins/ParcelScanListener.vue";
import ParcelScanType from "@/components/mixins/ParcelScanType.vue";
import Snackbar from "@/components/common/Snackbar.vue";
import ActiveSortJob from "@/components/sorter/ActiveSortJob.vue";
import { printPDF } from "@/utils/print.js";

export default {
  data: () => ({
    active_job_id: null,
    logistics_order: null
  }),
  mixins: [ParcelScanListener, ParcelScanType],
  components: {
    Snackbar,
    ActiveSortJob
  },
  mounted: function() {},
  computed: {},
  methods: {
    submitDirectParcel: function() {
      var vm = this;
      var parcel = vm.parcel_scan_info;
      if (!vm.validateParcel(parcel)) {
        return;
      }
      parcel["job_id"] = vm.active_job_id;
      vm.api
        .submitDirectShip(parcel.tracking_id, parcel)
        .then(resp => {
          vm.logistics_order = resp.logistics_order;
          printPDF(vm.logistics_order.label_url);
        })
        .catch(resp => {
          vm.$refs.Snackbar.showSnackbar("错误！", resp.description, "error");
        });
    },
    validateParcel: function(parcel) {
      var vm = this;
      var weight = parseFloat(parcel.weight);
      if (weight) {
        parcel.weight = weight;
      } else {
        vm.$refs.Snackbar.showSnackbar(
          "数据错误！",
          "重量错误，重量应为数字!",
          "error"
        );
        return false;
      }

      if (!parcel.tracking_id) {
        vm.$refs.Snackbar.showSnackbar(
          "数据错误！",
          "物流单号不能为空！",
          "error"
        );
        return false;
      }
      return true;
    }
  },
  watch: {
    tracking_id: {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.parcel_scan_info.tracking_id = newValue;
      }
    },
    weight: {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.parcel_scan_info.weight = newValue;
      }
    }
  }
};
</script>

<style lang="scss">
</style>
