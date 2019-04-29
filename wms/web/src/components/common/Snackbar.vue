<template>
  <div>
    <!-- <v-alert :value="alert_msg != null" :type="alert_type">{{ alert_msg }}</v-alert> -->
    <v-snackbar
      v-model="alert.show_alert"
      :timeout="1500"
      :top="true"
      :vertical="true"
      :auto-height="true"
      :color="alert.alert_type == 'success' ? 'success' : 'error'"
    >
      <h4>{{ alert.alert_title }}</h4>
      <div v-if="alert.alert_msg != null">{{ alert.alert_msg }}</div>
      <v-btn color="pink" flat @click="alert.show_alert = false">Close</v-btn>
    </v-snackbar>
  </div>
</template>

<script>
export default {
  data: () => ({
    alert: {
      alert_title: null,
      alert_msg: null,
      alert_type: "success",
      show_alert: false
    }
  }),
  mounted: function() {},
  computed: {},
  methods: {
    showSnackbar: function(title, msg, type) {
      var vm = this;
      vm.alert.alert_title = title;
      vm.alert.alert_msg = msg;
      vm.alert.show_alert = true;
      vm.alert.alert_type = type;
    }
  },
  watch: {}
};
</script>

<style lang="scss">
</style>
