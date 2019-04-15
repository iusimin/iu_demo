<script>
export default {
  props: ["value"],
  data: () => ({
    tracking_id: null,
    weight: null,
    sensitive_reason: null,
    has_battery: false,
    has_liquid: false
  }),
  mounted: function() {
    var vm = this;
    vm.tracking_id = vm.value.tracking_id || null;
    vm.weight = vm.value.weight || null;
  },
  methods: {
    updateParcelInfo: function() {
      var vm = this;
      vm.$emit("input", {
        tracking_id: vm.tracking_id,
        weight: vm.weight,
        sensitive_reason: vm.sensitive_reason,
        has_battery: vm.has_battery,
        has_liquid: vm.has_liquid
      });
    }
  },
  watch: {
    value: {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.tracking_id = newValue.tracking_id;
        vm.weight = newValue.weight;
      },
      deep: true
    },
    tracking_id: {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.updateParcelInfo();
      },
    },
    weight: {
      handler: function(newValue, oldValue) {
        var vm = this;
        vm.updateParcelInfo();
      },
    }
  }
};
</script>