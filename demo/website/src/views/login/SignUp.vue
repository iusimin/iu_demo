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
          color="green"
          title="Sign Up"
          text="Create a new account"
        >
          <v-form
            ref="form"
            v-model="valid"
            lazy-validation
          >
            <v-text-field
              v-model="username"
              :rules="[rules.required]"
              label="Username"
              required
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
            />
            <v-text-field
              v-model="password_confirm"
              :append-icon="showcpass ? 'mdi-eye' : 'mdi-eye-off'"
              :type="showcpass ? 'text' : 'password'"
              :rules="[rules.required, rules.min]"
              :error-messages="passwordConfirmError()"
              counter
              label="Verify Password"
              required
              @click:append="showcpass = !showcpass"
            />
            <v-text-field
              v-model="email"
              :rules="[rules.required, rules.email]"
              label="E-mail"
              required
            />
            <v-text-field
              v-model="phone_number"
              :rules="[rules.required]"
              label="Phone Number"
              required
            />
            <v-alert
              :value="error_msg"
              color="error"
              icon="mdi-alert-circle"
              outline
            >
              {{ error_msg }}
            </v-alert>
            <v-btn
              :disabled="!valid || signup_loading || signup_complete"
              :loading="signup_loading"
              color="info"
              @click="signUp"
            >
              {{ signup_btn_txt }}
              <v-icon
                v-if="signup_complete"
                dark
                right
              > mdi-checkbox-marked-circle </v-icon>
            </v-btn>
          </v-form>
        </material-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      // Fields
      username: '',
      password: '',
      password_confirm: '',
      email: '',
      phone_number: '',

      // For signup button
      signup_loading: null,
      signup_complete: null,
      signup_btn_txt: 'Sign Up',
      error_msg: null,

      valid: true,
      showpass: false,
      showcpass: false,
      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters',
        email: v => /.+@.+/.test(v) || 'E-mail must be valid'
      }
    }
  },
  methods: {
    validate () {
      if (this.$refs.form.validate()) {
        this.snackbar = true
      }
    },
    passwordConfirmError () {
      return (this.password === this.password_confirm) ? '' : 'Password not match'
    },
    signUp: function () {
      this.signup_loading = true
      this.error_msg = null
      axios
        .post(
          '/api/users',
          {
            username: this.username,
            password: this.password,
            email: this.email,
            phone_number: this.phone_number
          }
        )
        .then(
          response => {
            this.signup_loading = null
            this.signup_complete = true
            this.signup_btn_txt = 'Success'
          }
        )
        .catch(error => {
          this.signup_loading = null
          var data = error.response.data
          this.error_msg = data.title
          if (data.description) {
            this.error_msg += ' : ' + data.description
          }
        })
    }
  }
}
</script>
