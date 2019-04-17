<template>
  <v-container fluid>
    <v-alert :value="error_msg != null" type="error">{{ error_msg }}</v-alert>
    <v-form>
      <v-container>
        <v-layout row wrap>
          <v-flex md12>
            <v-text-field v-model="tracking_id" label="物流单号" required></v-text-field>
          </v-flex>
          <v-flex md12>
            <v-text-field v-model="weight" label="重量" required></v-text-field>
          </v-flex>
          <v-flex offset-md10 md2>
            <v-btn color="success" type="button" @click="submitDirectParcel">打单</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </v-form>
  </v-container>
</template>

<script>
import ParcelScanListener from "@/mixins/ParcelScanListener.vue";
import Vue from "vue";

export default {
  data: () => ({
      error_msg: null
  }),
  mixins: [ParcelScanListener],
  components: {},
  mounted: function() {},
  computed: {},
  methods: {
    submitDirectParcel: function() {}
  },
  watch: {}
};
</script>

<style lang="scss">
</style>
