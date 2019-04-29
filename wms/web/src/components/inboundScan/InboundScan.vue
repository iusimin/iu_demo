<template>
  <div>
    <v-container fluid>
      <!-- <v-alert :value="alert_msg != null" :type="alert_type">{{ alert_msg }}</v-alert> -->
      <v-snackbar
        v-model="show_alert"
        :timeout="1500"
        :top="true"
        :vertical="true"
        :auto-height="true"
        :color="alert_type == 'success' ? 'success' : 'error'"
      >
        <h4>{{ alert_title }}</h4>
        <div v-if="alert_msg != null">{{ alert_msg }}</div>
        <v-btn color="pink" flat @click="show_alert = false">Close</v-btn>
      </v-snackbar>
      <v-tabs centered color="cyan" dark grow icons-and-text @change="tabChanged">
        <v-tabs-slider color="yellow"></v-tabs-slider>

        <v-tab href="#tab-1">
          普货入库
          <v-icon>普货</v-icon>
        </v-tab>
        <v-tab href="#tab-2">
          特货入库
          <v-icon>特货</v-icon>
        </v-tab>
        <v-tab href="#tab-3">
          敏感货物入库
          <v-icon>敏感货物</v-icon>
        </v-tab>

        <v-tab-item value="tab-1">
          <ordinary-parcel v-model="parcel_map['tab-1']"></ordinary-parcel>
        </v-tab-item>
        <v-tab-item value="tab-2">
          <special-parcel v-model="parcel_map['tab-2']"></special-parcel>
        </v-tab-item>
        <v-tab-item value="tab-3">
          <sensitive-parcel v-model="parcel_map['tab-3']"></sensitive-parcel>
        </v-tab-item>
      </v-tabs>
    </v-container>
    <v-container>
      <v-flex class="offset-md10 md2">
        <v-btn class="font-weight-light" color="success" @click="submitParcel">提交</v-btn>
      </v-flex>
    </v-container>
  </div>
</template>

<script>
import OrdinaryParcel from "./OrdinaryParcel";
import SpecialParcel from "./SpecialParcel";
import SensitiveParcel from "./SensitiveParcel";
import ParcelScanListener from "@/mixins/ParcelScanListener.vue";
import Vue from "vue";

export default {
  data: () => ({
    alert_title: null,
    alert_msg: null,
    alert_type: "success",
    show_alert: false,
    current_tab: "tab-1",
    parcel_map: {
      "tab-1": {},
      "tab-2": {},
      "tab-3": {}
    },
    parcel_type_map: {
      "tab-1": 0, //TODO: use constant
      "tab-2": 1,
      "tab-3": 2
    }
  }),
  mixins: [ParcelScanListener],
  components: {
    OrdinaryParcel,
    SpecialParcel,
    SensitiveParcel
  },
  mounted: function() {},
  computed: {
    current_parcel: function() {
      var vm = this;
      return vm.parcel_map[vm.current_tab];
    }
  },
  methods: {
    tabChanged: function(tab_id) {
      var vm = this;
      vm.current_tab = tab_id;
    },
    submitParcel: function() {
      var vm = this;
      var parcel = vm.parcel_map[vm.current_tab];
      parcel.parcel_type = vm.parcel_type_map[vm.current_tab];
      if (!vm.validateParcel(parcel)) {
        return;
      }
      vm.api
        .inboundParcel(parcel.tracking_id, parcel)
        .then(resp => {
          vm.tracking_id = null;
          vm.weight = null;
          Vue.set(vm.parcel_map[vm.current_tab], "tracking_id", null);
          Vue.set(vm.parcel_map[vm.current_tab], "weight", null);
          vm.showSnackbar("成功入库！", "成功入库！", "success");
        })
        .catch(resp => {
          vm.tracking_id = null;
          vm.weight = null;
          Vue.set(vm.parcel_map[vm.current_tab], "tracking_id", null);
          Vue.set(vm.parcel_map[vm.current_tab], "weight", null);
          vm.showSnackbar("入库失败！", resp.description, "error");
        });
    },
    validateParcel: function(parcel) {
      var vm = this;
      var weight = parseFloat(parcel.weight);
      if (weight) {
        parcel.weight = weight;
      } else {
        vm.showSnackbar("数据错误！", "重量错误，重量应为数字!", "error");
        return false;
      }

      if (!parcel.tracking_id) {
        vm.showSnackbar("数据错误！", "物流单号不能为空！", "error");
        return false;
      }
      return true;
    },
    showSnackbar: function(title, msg, type) {
      var vm = this;
      vm.alert_title = title;
      vm.alert_msg = msg;
      vm.show_alert = true;
      vm.alert_type = type;
    },
    autoSubmitParcel: function() {
      var vm = this;
      var parcel = vm.parcel_map[vm.current_tab];
      var weight = parseFloat(parcel.weight);
      if (parcel.tracking_id && weight && vm.current_tab === "tab-1") {
        vm.submitParcel();
      }
    }
  },
  watch: {
    tracking_id: {
      handler: function(newValue, oldValue) {
        var vm = this;
        console.log("------");
        Vue.set(vm.parcel_map[vm.current_tab], "tracking_id", newValue);
        vm.autoSubmitParcel();
      }
    },
    weight: {
      handler: function(newValue, oldValue) {
        var vm = this;
        Vue.set(vm.parcel_map[vm.current_tab], "weight", newValue);
        vm.autoSubmitParcel();
      }
    }
  }
};
</script>

<style lang="scss">
</style>
