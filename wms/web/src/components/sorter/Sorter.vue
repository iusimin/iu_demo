<template>
  <v-container fluid grid-list-xl>
    <v-layout wrap>
      <v-flex md12 lg12>
        <active-sort-job v-model="active_job_id"></active-sort-job>
      </v-flex>
      <v-flex md12 lg12>
        <v-stepper v-model="round_id" vertical>
          <v-stepper-step :complete="round_id > 1" step="1">第一次分拣</v-stepper-step>
          <v-stepper-content step="1">
            <sort-step v-model="parcel_infos[1]" :round_id="1" :job_id="active_job_id"></sort-step>
            <v-btn color="primary" @click="round_id = 2">继续下一轮分拣</v-btn>
          </v-stepper-content>

          <v-stepper-step :complete="round_id > 2" step="2">第二次分拣</v-stepper-step>
          <v-stepper-content step="2">
            <sort-step v-model="parcel_infos[2]" :round_id="2" :job_id="active_job_id"></sort-step>
            <v-btn color="primary" @click="round_id = 3">继续下一轮分拣</v-btn>
          </v-stepper-content>

          <v-stepper-step :complete="round_id > 3" step="3">第三次分拣</v-stepper-step>
          <v-stepper-content step="3">
            <sort-step v-model="parcel_infos[3]" :round_id="3" :job_id="active_job_id"></sort-step>
          </v-stepper-content>
        </v-stepper>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import SortStep from "@/components/sorter/SortStep.vue";
import ParcelScanListener from "@/components/mixins/ParcelScanListener.vue";
import ActiveSortJob from "@/components/sorter/ActiveSortJob.vue";
import Vue from "vue";

export default {
  data: () => ({
    active_job_id: null,
    round_id: 1,
    parcel_infos: {
      1: {},
      2: {},
      3: {}
    }
  }),
  mixins: [ParcelScanListener],
  components: {
    SortStep,
    ActiveSortJob
  },
  methods: {},
  watch: {
    tracking_id: {
      handler: function(newValue, oldValue) {
        var vm = this;
        Vue.set(vm.parcel_infos[vm.round_id], "tracking_id", newValue);
      }
    }
  }
};
</script>

<style lang="scss">
</style>
