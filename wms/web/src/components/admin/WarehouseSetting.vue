<template>
  <v-container fluid>
    <v-alert :value="error_msg != null" type="error">{{ error_msg }}</v-alert>
    <v-form>
      <v-container>
        <v-layout row wrap>
          <v-flex md12>
            <p class="display-1">{{ "CHINAPOST-DONGGUAN" }}</p>
          </v-flex>
          <v-flex md12>
            <p class="title">称重单位设置</p>
          </v-flex>
          <v-flex md12>
            <v-select :items="['克', '千克']" label="称重单位" v-model="weight_unit"></v-select>
          </v-flex>
          <v-flex md12>
            <p class="title">播种柜设置</p>
          </v-flex>
          <v-flex md3>
            <v-text-field v-model="cabinet_count" label="架子数量" placeholder="架子数量" required></v-text-field>
          </v-flex>
          <v-flex md3>
            <v-select :items="['横向', '纵向']" label="格口方向" v-model="cabinet_orientation"></v-select>
          </v-flex>
          <v-flex md3>
            <v-select :items="[1,2,3,4,5,6,7,8,9]" label="行数" v-model="cabinet_height"></v-select>
          </v-flex>
          <v-flex md3>
            <v-select :items="[1,2,3,4,5,6,7,8,9]" label="列数" v-model="cabinet_width"></v-select>
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
export default {
  data: () => ({
    error_msg: null,
    weight_unit: "克",
    cabinet_count: 8,
    cabinet_orientation: "横向",
    cabinet_height: 5,
    cabinet_width: 8
  }),
  mounted: function() {},
  methods: {
    submitWarehouseSetting: function() {}
  }
};
</script>

<style lang="scss">
</style>
