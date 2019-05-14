<template>
  <div>
    <active-sort-job v-model="active_job_id"></active-sort-job>
    <v-container fluid grid-list-xl>
      <v-stepper v-model="e1">
        <v-stepper-header>
          <v-stepper-step :complete="e1 > 1" step="1">播种</v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step :complete="e1 > 2" step="2">合并打单</v-stepper-step>
        </v-stepper-header>
        <seed :job_id="active_job_id" :mode="mode"></seed>
        <v-stepper-items>
          <v-stepper-content step="1">
            <v-btn color="primary" @click="goToCombine">全部上架完成</v-btn>
          </v-stepper-content>
          <v-stepper-content step="2">
            <v-btn color="secondary" @click="goToSeed">继续播种</v-btn>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-container>
  </div>
</template>

<script>
import Seed from "./Seed";
import Combine from "./Combine";
import ActiveSortJob from "@/components/sorter/ActiveSortJob.vue";
import { mapMutations } from "vuex";
import { MutationNames } from "@/store/constants.js";

export default {
  data: () => ({
    e1: 1,
    active_job_id: null
  }),
  components: {
    Seed,
    Combine,
    ActiveSortJob
  },
  methods: {
    ...mapMutations([MutationNames.SET_SEED_MODE]),
    goToCombine: function() {
      var vm = this;
      vm.e1 = 2;
      vm.$store.commit(MutationNames.SET_SEED_MODE, 1);
    },
    goToSeed: function() {
      var vm = this;
      vm.e1 = 1;
      vm.mode = 0;
      vm.$store.commit(MutationNames.SET_SEED_MODE, 0);
    }
  }
};
</script>

<style lang="scss">
</style>
