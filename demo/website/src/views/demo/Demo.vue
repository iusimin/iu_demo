<template>
  <v-container
    fill-height
    fluid
    grid-list-xl>
    <v-layout
      justify-center
      wrap
    >
      <v-flex
        xs12
        md8
      >
        <material-card
          color="green"
          title="IU Demo Cases"
          text=""
        >
          <v-form>
            <v-container py-0>
              <v-layout wrap>
                <v-flex
                  xs12
                  text-xs-right
                >
                  <v-btn
                    class="mx-0 font-weight-light"
                    color="success"
                  >
                    Simulate long running mongo query
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-container>
          </v-form>
        </material-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Login from '@/components/mixins/Login.vue'
export default {
  mixins: [Login],
  data: () => ({
    require_login: true
  }),
  beforeRouteUpdate (to, from, next) {
    if (this.require_login && !this.loginUsername) {
      next('/login')
    } else {
      next()
    }
  }
}
</script>
