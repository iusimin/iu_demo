<script>
export default {
  props: ["value"],
  data: () => ({
    parcel_scan_info: {
      tracking_id: null,
      weight: null,
      sensitive_reason: null,
      has_battery: false,
      has_liquid: false
    }
  }),
  mounted: function() {
    var vm = this;
    if (vm.value) {
      Object.assign(vm.parcel_scan_info, vm.value);
    }
    var eles = document.getElementsByClassName("stop-propagation");
    for (let i = 0; i < eles.length; i++) {
      eles[i].addEventListener("keyup", vm.stopInputPropagation);
    }
  },
  methods: {
    updateParcelInfo: function() {
      var vm = this;
      vm.$emit("input", vm.parcel_scan_info);
    },
    stopInputPropagation: function(e) {
      e.stopPropagation();
    }
  },
  watch: {
    value: {
      handler: function(newValue, oldValue) {
        var vm = this;
        Object.assign(vm.parcel_scan_info, vm.value);
      },
      deep: true
    },
    parcel_scan_info: {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.updateParcelInfo();
      },
      deep: true
    }
  },
  destroyed: function() {
    var vm = this;
    var eles = document.getElementsByClassName("stop-propagation");
    for (let i = 0; i < eles.length; i++) {
      eles[i].removeEventListener("keyup", vm.stopInputPropagation);
    }
  }
};
</script>