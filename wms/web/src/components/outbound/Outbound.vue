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

        <v-stepper-items>
          <v-stepper-content step="1">
            <seed :job_id="active_job_id"></seed>
            <v-btn color="primary" @click="e1 = 2">全部上架完成</v-btn>
          </v-stepper-content>
          <v-stepper-content step="2">
            <combine></combine>
          </v-stepper-content>
        </v-stepper-items>
        <!-- <v-stepper-step :complete="e1 > 1" step="1">播种</v-stepper-step>

          <v-stepper-content step="1">
            <seed></seed>
            <v-btn color="primary" @click="e1 = 2">Continue</v-btn>
          </v-stepper-content>

          <v-stepper-step :complete="e1 > 2" step="2">合并打单</v-stepper-step>

          <v-stepper-content step="2">
            <combine></combine>
            <v-btn color="primary">Continue</v-btn>
        </v-stepper-content>-->
      </v-stepper>
    </v-container>
  </div>
</template>

<script>
import Seed from "./Seed";
import Combine from "./Combine";
import ActiveSortJob from "@/components/sorter/ActiveSortJob.vue";

export default {
  data: () => ({
    e1: 1,
    active_job_id: null
  }),
  components: {
    Seed,
    Combine,
    ActiveSortJob
  }
};
</script>

<style lang="scss">
</style>
