<template>
  <v-container fluid grid-list-xl>
    <div style="margin: -40px 0px;">
      <v-layout wrap>
        <v-flex md12 lg12 v-if="has_active_job">
          <v-alert
            type="success"
            v-model="has_active_job"
            color="success"
            icon="mdi-anchor"
          >
            <span class="font-weight-black title">当前分拣任务：{{ active_job_id }}</span>
          </v-alert>
        </v-flex>

        <v-flex md12 lg12 v-if="no_active_job">
          <v-alert
            type="warning"
            v-model="no_active_job"
            color="warning"
            icon="mdi-anchor"
          >
            <span class="font-weight-black title">{{ no_job_message }}</span>
          </v-alert>
        </v-flex>
      </v-layout>
    </div>
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
      vm.api
        .getActiveSortJob()
        .then(resp => {
          vm.active_job = resp.job;
        })
        .catch(resp => {
          vm.no_job_message = resp.description;
        });
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
