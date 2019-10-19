<template>
  <div fluid>
    <v-layout v-for="i in size_y" :key="i">
      <v-flex v-for="j in size_x" :key="j">
        <div style="margin: -10px;">
          <lattice ref="Lattices" :lattice_info="get_cabinet_info((i - 1) * size_x + j)"></lattice>
        </div>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
//TODO antony: refactor later.
import { mapState } from "vuex";
import Lattice from "./Lattice";
export default {
  data: () => ({
    cabinet_infos: []
  }),
  props: ["parcels", "size_x", "size_y"],
  components: {
    Lattice
  },
  computed: {
    ...mapState(["seed_mode"])
  },
  methods: {
    reset: function(parcels_by_combine_id) {
      var vm = this;
      vm.cabinet_infos = [];
      parcels_by_combine_id.forEach(function(parcels) {
        vm.cabinet_infos.push({
          total_count: parcels.length,
          parcels: parcels
        });
      });
      vm.$refs.Lattices.forEach(function(lattice, i) {
        lattice.reset(vm.get_cabinet_info(i));
      });
    },
    get_cabinet_info: function(index) {
      var vm = this;
      var cabinet_info = vm.cabinet_infos[index];
      if (!cabinet_info) {
        cabinet_info = {
          total_count: 0
        };
      }
      cabinet_info["index"] = ("0" + (index + 1)).slice(-2);
      return cabinet_info;
    },
    seed_parcel: function(parcel) {
      var vm = this;
      vm.$refs.Lattices.forEach(function(lattice) {
        lattice.reset_color();
      });
      var lattice_id = parcel.lattice_id;
      var lattice = vm.$refs.Lattices[lattice_id - 1];
      lattice.add_parcel(parcel);
    },
    combineScannedParcel: function(parcel) {
      var vm = this;
      vm.$refs.Lattices.forEach(function(lattice) {
        lattice.resetCombineColor();
      });
      var lattice_id = parcel.lattice_id;
      var lattice = vm.$refs.Lattices[lattice_id - 1];
      lattice.combineScannedParcel(parcel);
    }
  },
  watch: {
    seed_mode: {
      handler: function(newValue, oldValue) {
        var vm = this;
        if (oldValue == 0 && newValue == 1) {
          vm.$refs.Lattices.forEach(function(lattice) {
            lattice.enterCombineMode();
          });
        }
        if (oldValue == 1 && newValue == 0) {
          vm.$refs.Lattices.forEach(function(lattice) {
            lattice.enterSeedMode();
          });
        }
      }
    }
  }
};
</script>

<style lang="scss">
</style>
