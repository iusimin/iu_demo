<template>
  <div style="padding: 2px;">
    <v-card ref="LatticeCard" v-bind:style="card_style">
      <v-card-text>
        <v-layout align-center justify-center column>
          <div class="font-weight-medium headline">{{ lattice_info ? lattice_info.index : null }}</div>
          <div>{{ progress }}</div>
        </v-layout>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  data: () => ({
    lattice_info: null,
    seeded_parcels: {},
    card_style: {
      "background-color": "#B39DDB"
    },
    seeded_count: 0,
    mode: 0, //0 for seed, 1 for combine
    combine_scanned_parcels: {}
  }),
  props: [],
  components: {},
  computed: {
    progress: function() {
      var vm = this;
      var res = "";
      if (vm.lattice_info) {
        res = vm.seeded_count + " / " + vm.lattice_info.total_count;
      }
      return res;
    }
  },
  mounted: function() {
    var vm = this;
    vm.reset_color();
  },
  methods: {
    add_parcel: function(parcel) {
      var vm = this;
      if (parcel) {
        vm.seeded_parcels[parcel.tracking_id] = parcel;
        vm.calculate_seeded_count();
      }
      vm.hightlight();
    },
    reset: function(lattice_info) {
      var vm = this;
      vm.lattice_info = lattice_info;
      vm.seeded_parcels = {};
      vm.calculate_seeded_count();
      vm.reset_color();
    },
    reset_color: function() {
      var vm = this;
      vm.card_style["background-color"] = "#B39DDB"; // TODO: use color from theme
      if (vm.lattice_info && vm.seeded_count == vm.lattice_info.total_count) {
        vm.card_style["background-color"] = "#43A047";
      }
    },
    hightlight: function() {
      var vm = this;
      vm.card_style["background-color"] = "#F50057";
    },
    calculate_seeded_count: function() {
      var vm = this;
      var seeded_count = 0;
      for (let k in vm.seeded_parcels) {
        if (vm.seeded_parcels.hasOwnProperty(k)) {
          seeded_count += 1;
        }
      }
      vm.seeded_count = seeded_count;
    },

    //Combine parcels
    combine_scanned_parcel: function(parcel) {
      var vm = this;
      if (parcel) {
        vm.combine_scanned_parcels[parcel.tracking_id] = parcel;
      }
    }
  }
};
</script>

<style lang="scss">
</style>
