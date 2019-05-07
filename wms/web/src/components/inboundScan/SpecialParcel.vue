<template>
  <v-container fluid>
    <v-alert :value="error_msg != null" type="error">{{ error_msg }}</v-alert>
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
          <v-flex md12>
            <v-checkbox
              class="stop-propagation"
              v-model="parcel_scan_info.has_battery"
              label="是否带电"
            ></v-checkbox>
          </v-flex>
          <v-flex md12>
            <v-checkbox
              class="stop-propagation"
              v-model="parcel_scan_info.has_liquid"
              label="是否带液体"
            ></v-checkbox>
          </v-flex>
        </v-layout>
      </v-container>
    </v-form>
  </v-container>
</template>

<script>
import ParcelScanType from "@/components/mixins/ParcelScanType.vue";
export default {
  data: () => ({
    error_msg: null
  }),
  mixins: [ParcelScanType],
  mounted: function() {},
  methods: {}
};
</script>

<style lang="scss">
</style>
