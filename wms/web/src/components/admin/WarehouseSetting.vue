<template>
  <v-container fluid>
    <snackbar ref="Snackbar"></snackbar>
    <v-form ref="WarehouseSetting">
      <v-container>
        <v-layout row wrap>
          <v-flex md12>
            <p class="display-1">{{ operator_warehouse.warehouse_name }}</p>
          </v-flex>
          <v-flex md12>
            <p class="title">称重单位设置</p>
          </v-flex>
          <v-flex md12>
            <v-select
              :items="WarehouseWeightUnits"
              label="称重单位"
              v-model="operator_warehouse.weight_unit"
            ></v-select>
          </v-flex>
          <v-flex md12>
            <p class="title">播种柜设置</p>
          </v-flex>
          <v-flex md3>
            <v-text-field
              v-model="operator_warehouse.cabinet_count"
              label="架子数量"
              placeholder="架子数量"
              required
            ></v-text-field>
          </v-flex>
          <v-flex md3>
            <v-select
              :items="CabinetOrientation"
              label="格口方向"
              v-model="operator_warehouse.cabinet_orientation"
            ></v-select>
          </v-flex>
          <v-flex md3>
            <v-select
              :items="CabinetSize"
              label="行数"
              v-model="operator_warehouse.cabinet_size.height"
            ></v-select>
          </v-flex>
          <v-flex md3>
            <v-select
              :items="CabinetSize"
              label="列数"
              v-model="operator_warehouse.cabinet_size.width"
            ></v-select>
          </v-flex>
          <v-flex offset-md10 md2>
            <v-btn color="success" type="button" @click="submitWarehouseSetting">提交修改</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </v-form>
  </v-container>
</template>

<script>
import {
  WarehouseWeightUnits,
  CabinetOrientation,
  CabinetSize
} from "@/constants/constants.js";
import Snackbar from "@/components/common/Snackbar.vue";
export default {
  data: () => ({
    WarehouseWeightUnits: WarehouseWeightUnits,
    CabinetOrientation: CabinetOrientation,
    CabinetSize: CabinetSize,
    operator_warehouse: {
      weight_unit: null,
      cabinet_count: null,
      cabinet_orientation: null,
      cabinet_size: {
        height: null,
        width: null
      }
    }
  }),
  mounted: function() {
    var vm = this;
    vm.api.getOperatorWarehouse().then(resp => {
      vm.operator_warehouse = resp.warehouse;
    });
  },
  computed: {},
  components: {
    Snackbar
  },
  methods: {
    submitWarehouseSetting: function() {
      var vm = this;
      vm.validateSetting();
      vm.api
        .updateOperatorWarehouseSetting(
          vm.operator_warehouse.warehouse_id,
          vm.operator_warehouse
        )
        .then(resp => {
          vm.$refs.Snackbar.showSnackbar("成功", "提交成功！", "success");
        })
        .catch(resp => {
          alert("error");
        });
    },
    validateSetting: function() {
      var vm = this;
      var res = vm.$refs.WarehouseSetting.validate();
      console.log(res);
    }
  }
};
</script>

<style lang="scss">
</style>
