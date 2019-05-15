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
          title="Your Profile"
          text=""
        >
          <v-form
            ref="form"
            v-model="valid"
            lazy-validation
          >
            <v-text-field
              v-model="loginUsername"
              label="Username"
            />
            <v-text-field
              v-model="email"
              label="E-mail"
            />
            <v-text-field
              v-model="phone_number"
              label="Phone Number"
            />
          </v-form>
        </material-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Base from '@/mixins/Base.vue'
import axios from 'axios'
export default {
  mixins: [Base],
  data: () => ({
    email: null,
    phone_number: null
  }),
  mounted () {
    this.getUserProfile()
  },
  methods: {
    getUserProfile () {
      axios.get(
        `api/user/${this.loginUserId}`,
        {}
      ).then(response => {
        var data = response.data
        this.email = data.email
        this.phone_number = data.phone_number
      }).catch(error => {
        alert(error.response.data.title)
      })
    }
  }
}
</script>
