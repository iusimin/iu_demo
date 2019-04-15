<script>
export default {
  data: () => ({
    tracking_id: null,
    weight: null,
    key_pressed: ""
  }),
  mounted: function() {
    var vm = this;
    window.addEventListener("keyup", vm.keyUpHandler);
  },
  methods: {
    keyUpHandler: function(e) {
      var vm = this;
      console.log(e.key);
      if (e.which != 13) {
        vm.key_pressed += e.key;
      } else {
        vm.checkInput();
      }
    },
    checkInput: function() {
      var vm = this;
      var val = parseFloat(vm.key_pressed);
      if (val) {
        vm.weight = val;
      } else {
        vm.tracking_id = vm.key_pressed;
      }
      vm.key_pressed = "";
    }
  },
  destroyed: function() {
    var vm = this;
    window.removeEventListener("keyup", vm.keyUpHandler);
  }
};
</script>