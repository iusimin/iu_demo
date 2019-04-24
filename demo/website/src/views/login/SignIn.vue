<template>
  <v-container
    fill-height
    fluid
    grid-list-xl
  >
    <v-layout
      justify-center
      wrap
    >
      <v-flex
        md4
      >
        <material-card
          v-if="!loginUsername"
          color="green"
          title="Sign In"
          text="Sign in your account"
        >
          <v-form
            ref="form"
            v-model="valid"
          >
            <v-text-field
              v-model="username"
              :rules="[rules.required]"
              label="Username"
              required
              @keyup.enter="signIn"
            />
            <v-text-field
              v-model="password"
              :append-icon="showpass ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showpass ? 'text' : 'password'"
              :rules="[rules.required, rules.min]"
              hint="At least 8 characters"
              counter
              label="Password"
              required
              @click:append="showpass = !showpass"
              @keyup.enter="signIn"
            />
            <v-btn
              :disabled="!valid || signin_loading"
              color="success"
              @click="signIn"
            >
              Sign In
            </v-btn>
            <router-link to="/signup">
              <v-btn
                color="info"
              >
                Sign Up
              </v-btn>
            </router-link>
          </v-form>
        </material-card>
        <material-card
          v-if="loginUsername"
          color="green"
          title="Change account"
          text="Change your login account"
        >
          Hello, {{ loginUsername }}.
          </br>
          <v-btn
            :disabled="signout_loading"
            color="warning"
            @click="signOut"
          >
            Sign Out
          </v-btn>
        </material-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'
import Base from '@/components/mixins/Base.vue'
export default {
  mixins: [Base],
  data () {
    return {
      // Fields
      username: '',
      password: '',

      valid: true,
      showpass: false,
      signin_loading: null,
      signout_loading: null,
      error_msg: null,
      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters'
      }
    }
  },
  methods: {
    validate () {
      if (this.$refs.form.validate()) {
        this.snackbar = true
      }
    },
    signIn () {
      this.signin_loading = true
      this.error_msg = null
      axios
        .post(
          '/api/login',
          {
            username: this.username,
            password: this.password
          }
        )
        .then(
          response => {
            var data = response.data
            this.signin_loading = null
            this.loginUserId = data.user_id
            this.loginUsername = data.username
            this.loginPermissions = data.permissions
            if (this.$route.query.redirect) {
              this.$router.push({
                path: this.$route.query.redirect
              })
            } else {
              this.$router.push({
                path: '/'
              })
            }
          }
        )
        .catch(error => {
          this.signin_loading = null
          var data = error.response.data
          this.error_msg = data.title
          if (data.description) {
            this.error_msg += ' : ' + data.description
          }
          alert(this.error_msg)
        })
    },
    signOut () {
      this.signout_loading = true
      this.error_msg = null
      axios
        .delete(
          '/api/login',
          {}
        )
        .then(
          response => {
            this.signout_loading = null
            this.loginUserId = null
            this.loginUsername = null
            this.loginPermissions = null
            alert(response.data.title)
            this.$router.push({
              path: '/'
            })
          }
        )
        .catch(error => {
          this.signout_loading = null
          var data = error.response.data
          this.error_msg = data.title
          if (data.description) {
            this.error_msg += ' : ' + data.description
          }
          alert(this.error_msg)
        })
    }
  }
}
</script>
