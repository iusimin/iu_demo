<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>登录</v-toolbar-title>
              <v-spacer></v-spacer>
              <!-- <v-tooltip bottom>
                <v-icon slot="activator">mdi-account</v-icon>
                <span>mdi-account</span>
              </v-tooltip> -->
            </v-toolbar>
            <v-card-text>
              <v-form>
                <v-text-field prepend-icon="mdi-account" name="login" label="Login" type="text" v-model="username"></v-text-field>
                <v-text-field
                  prepend-icon="mdi-lock-question"
                  name="password"
                  label="Password"
                  id="password"
                  type="password"
                  v-model="password"
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="login">Login</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script>
export default {
  data: () => ({
    username: null,
    password: null,
    return_url: null
  }),
  props: [],
  components: {},
  computed: {},
  methods: {
    login: function() {
      var vm = this;
      vm.api.login(
        vm.username,
        vm.password,
        false,
        resp => {
          var redirect = vm.$route.query.redirect || '/home';
          vm.$router.push(redirect);
        },
        resp => {
          alert("failed");
        }
      );
    }
  }
};
</script>

<style lang="scss">
</style>
