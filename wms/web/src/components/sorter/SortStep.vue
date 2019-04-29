<template>
  <v-container fluid>
    <!-- <v-alert :value="alert_msg != null" type="error">{{ alert_msg }}</v-alert> -->
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
        </v-layout>
      </v-container>
    </v-form>
    <div>
      <v-card>
        <v-card-text>
          <p class="display-4 font-weight-black text-md-center">{{ sort_info.round_group_id }}</p>
          <v-text-field v-model="sort_info.weight" label="weight" :readonly="true"></v-text-field>
          <v-text-field
            v-model="sort_info.inbound_datetime"
            label="inbound datetime"
            :readonly="true"
          ></v-text-field>
        </v-card-text>
      </v-card>
    </div>
    <v-snackbar
      v-model="show_alert"
      :timeout="1500"
      :top="true"
      :vertical="true"
      :auto-height="true"
      :color="alert_type == 'success' ? 'success' : 'error'"
    >
      <div v-if="alert_msg != null">{{ alert_msg }}</div>
      <v-btn color="pink" flat @click="show_alert = false">Close</v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
import ParcelScanType from "@/mixins/ParcelScanType.vue";
export default {
  props: ["round_id", "job_id"],
  data: () => ({
    show_alert: false,
    alert_msg: null,
    sort_info: {
      round_group_id: null,
      weight: null,
      inbound_datetime: null
    }
  }),
  mounted: function() {},
  mixins: [ParcelScanType],
  methods: {
    getSortInfo: function() {
      var vm = this;
      vm.api
        .getParcelSortInfo(
          vm.parcel_scan_info.tracking_id,
          vm.job_id,
          vm.round_id
        )
        .then(resp => {
          vm.sort_info = resp.sort_info;
        })
        .catch(resp => {
          vm.sort_info.round_group_id = null;
          vm.sort_info.weight = null;
          vm.sort_info.inbound_datetime = null;
          vm.show_alert = true;
          vm.alert_msg = resp.description;
        });
    }
  },
  watch: {
    "parcel_scan_info.tracking_id": {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.getSortInfo();
      },
      deep: true
    }
  }
};
</script>

<style lang="scss">
</style>
