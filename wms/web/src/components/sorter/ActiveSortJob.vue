<template>
  <v-container fluid grid-list-xl>
    <v-layout wrap>
      <v-flex md12 lg12 v-if="has_active_job">
        <v-alert
          v-model="has_active_job"
          color="success"
          icon="mdi-anchor"
          outline
        ><span class="font-weight-black title">{{ active_job_id }}</span></v-alert>
      </v-flex>

      <v-flex md12 lg12 v-if="no_active_job">
        <v-alert
          v-model="no_active_job"
          color="warning"
          icon="priority_high"
          outline
        >{{ no_job_message }}</v-alert>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  props: ["value"],
  data: () => ({
    active_job: null,
    no_job_message: null
  }),
  computed: {
    active_job_id: function() {
      var vm = this;
      return vm.active_job != null ? vm.active_job.job_id : null;
    },
    has_active_job: function() {
      var vm = this;
      return vm.active_job_id != null;
    },
    no_active_job: function() {
      var vm = this;
      return !vm.has_active_job;
    }
  },
  mounted() {
    var vm = this;
    vm.getActiveSortJob();
  },
  components: {},
  methods: {
    getActiveSortJob: function() {
      var vm = this;
      vm.api.getActiveSortJob(
        resp => {
          vm.active_job = resp.job;
        },
        resp => {
          vm.no_job_message = resp.description;
        }
      );
    }
  },
  watch: {
    active_job_id: {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.$emit("input", newValue);
      }
    }
  }
};
</script>

<style lang="scss">
</style>
