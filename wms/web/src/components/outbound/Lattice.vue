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
import { mapState } from 'vuex';
import Vue from "vue";

export default {
  data: () => ({
    lattice_info: null,
    seeded_parcels: {},
    combine_scanned_parcels: {},
    card_style: {
      "background-color": "primary"
    }
  }),
  props: [],
  components: {},
  computed: {
    ...mapState(['seed_mode']),
    seeded_count: function() {
      var vm = this;
      var seeded_count = 0;
      for (let k in vm.seeded_parcels) {
        if (vm.seeded_parcels.hasOwnProperty(k)) {
          seeded_count += 1;
        }
      }
      return seeded_count;
    },
    combine_scanned_count: function() {
      var vm = this;
      var count = 0;
      for (let k in vm.combine_scanned_parcels) {
        if (vm.combine_scanned_parcels.hasOwnProperty(k)) {
          count += 1;
        }
      }
      return count;
    },
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
        Vue.set(vm.seeded_parcels, parcel.tracking_id, parcel);
      }
      vm.hightlight();
    },
    reset: function(lattice_info) {
      var vm = this;
      vm.lattice_info = lattice_info;
      vm.seeded_parcels = {};
      //vm.calculate_seeded_count();
      vm.reset_color();
    },
    reset_color: function() {
      var vm = this;
      vm.card_style["background-color"] = "#B39DDB";
      if (vm.lattice_info && vm.seeded_count == vm.lattice_info.total_count) {
        vm.card_style["background-color"] = "#43A047";
      }
    },
    hightlight: function() {
      var vm = this;
      vm.card_style["background-color"] = "#F50057";
    },

    enterSeedMode: function() {
      var vm = this;
      vm.seeded_parcels = {};
      vm.combine_scanned_parcels = {};
      vm.reset_color();
    },
    checkMode: function(expected_mode) {
      var vm = this;
      if (vm.seed_mode != expected_mode) {
        return false;
      }
      return true;
    },

    //Combine parcels
    enterCombineMode: function() {
      var vm = this;
      vm.card_style["background-color"] = "#7CB342";
    },
    combineScannedParcel: function(parcel) {
      var vm = this;
      if (parcel) {
        Vue.set(vm.combine_scanned_parcels, parcel.tracking_id, parcel);
        vm.hightlight();
      }
    },
    resetCombineColor: function() {
      var vm = this;
      vm.card_style["background-color"] = "#7CB342";
      if (vm.lattice_info && vm.combine_scanned_count == vm.lattice_info.total_count) {
        vm.card_style["background-color"] = "#2E7D32";
      }
    }
  }
};
</script>

<style lang="scss">
</style>
