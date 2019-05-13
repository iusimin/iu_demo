<template>
  <v-container fluid>
    <v-layout v-for="i in size_y" :key="i">
      <v-flex v-for="j in size_x" :key="j">
        <lattice ref="Lattices" :lattice_info="get_cabinet_info((i - 1) * size_y + j)"></lattice>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Lattice from "./Lattice";
export default {
  data: () => ({
    cabinet_infos: []
  }),
  props: ["parcels", "size_x", "size_y"],
  components: {
    Lattice
  },
  computed: {},
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
      var lattice_id = parcel.lattice_id;
      var lattice = vm.$refs.Lattices[lattice_id - 1];
      vm.$refs.Lattices.forEach(function(lattice) {
        lattice.reset_color();
      });
      lattice.add_parcel(parcel);
    },
    combine_scanned_parcel: function(parcel) {
      var vm = this;
      var lattice_id = parcel.lattice_id;
      var lattice = vm.$refs.Lattices[lattice_id - 1];
      lattice.combine_scanned_parcel(parcel);
    }
  }
};
</script>

<style lang="scss">
</style>
