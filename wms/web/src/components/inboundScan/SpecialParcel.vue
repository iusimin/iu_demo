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
          <v-flex md12>
            <v-checkbox v-model="has_battery" label="是否带电"></v-checkbox>
          </v-flex>
          <v-flex md12>
            <v-checkbox v-model="has_liquid" label="是否带液体"></v-checkbox>
          </v-flex>
        </v-layout>
      </v-container>
    </v-form>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    tracking_id: null,
    weight: null,
    has_battery: false,
    has_liquid: false,
    error_msg: null
  })
}
</script>

<style lang="scss">
</style>
