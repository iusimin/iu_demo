<template>
  <v-container
    fill-height
    fluid
  >
    <v-layout
      justify-center
      align-center
    >
      <v-flex xs12>
        <v-card-text>
          <h2 class="font-weight-light mb-4">{{code}} {{ error.name }}</h2>
          <p v-if="error.hint"> {{ error.hint }} </p>
        </v-card-text>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>

export default {
  data: () => ({
    http_code: {
      400: {
        'name': 'Bad Request'
      },
      401: {
        'name': 'Unauthorized'
      },
      403: {
        'name': 'Forbidden'
      },
      404: {
        'name': 'Not Found',
        'hint': 'Please check URL'
      },
      500: {
        'name': 'Internal Server Error'
      },
      '*': {
        'name': 'Unknown'
      }
    }
  }),
  computed: {
    code () {
      return this.$route.params.code
    },
    error () {
      return this.http_code[this.code] || this.http_code['*']
    },
    hint () {
      return this.$route.query.hint || this.error.hint
    }
  }
}
</script>