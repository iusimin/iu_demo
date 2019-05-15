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
          title="Async access demo"
          text="Simulate long running mongo query"
        >
          <v-form
            ref="sleep_form"
            v-model="sleep_form_valid"
            @submit="submit"
            onSubmit="return false;"
          >
            <v-container py-0>
              <v-layout wrap>
                <v-flex
                  xs12
                  md8
                >
                  <v-text-field
                    v-model.number="sleep_seconds"
                    :rules="[rules.required, rules.above_zero]"
                    label="Sleeping seconds"
                    required
                    @keyup.enter="mongoSleep"
                  />
                </v-flex>
                <v-flex
                  xs12
                  md4
                  text-xs-right
                >
                  <v-btn
                    :disabled="!sleep_form_valid || sleep_loading"
                    :loading="sleep_loading"
                    class="mx-0 font-weight-light"
                    color="success"
                    @click="mongoSleep"
                  >
                    {{ sleep_btn_text }}
                  </v-btn>
                </v-flex>
              </v-layout>
            </v-container>
          </v-form>
        </material-card>
        <material-card
          color="blue"
          title="Async task demo"
          text="Push async task to BE queue"
        >
          <v-form
            ref="task_form"
            v-model="task_form_valid"
            @submit="submit"
            onSubmit="return false;"
          >
            <v-container py-0>
              <v-layout wrap>
                <v-flex
                  xs12
                  md4
                >
                  <v-text-field
                    v-model="light_count"
                    class="purple-input"
                    label="Push light task (count)"
                    :rules="[rules.required, rules.above_zero]"
                    @keyup.enter="publishAsyncTask"
                  />
                </v-flex>
                <v-flex
                  xs12
                  md4
                >
                  <v-text-field
                    v-model="heavy_count"
                    class="purple-input"
                    label="Push heavy task (count)"
                    :rules="[rules.required, rules.above_zero]"
                    @keyup.enter="publishAsyncTask"
                  />
                </v-flex>
                <v-flex
                  xs12
                  md4
                  text-xs-right
                >
                  <v-btn
                    :disabled="!task_form_valid || task_loading"
                    :loading="task_loading"
                    class="mx-0 font-weight-light"
                    color="info"
                    @click="publishAsyncTask"
                  >
                    Go
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
import axios from 'axios'
import Base from '@/mixins/Base.vue'
export default {
  mixins: [Base],
  data () {
    return {
      // For mongo sleep demo
      sleep_form_valid: null,
      sleep_seconds: null,
      sleep_form_valid: true,
      sleep_btn_text: 'Go',
      sleep_loading: false,

      // For async task demo
      task_form_valid: null,
      light_count: null,
      heavy_count: null,
      task_loading: false,

      rules: {
        required: value => !!value || 'Required.',
        min: v => v.length >= 8 || 'Min 8 characters',
        above_zero: v => Number(v) > 0 || 'Must be >0 integer'
      }
    }
  },
  mounted() {
    console.log(this.loginUserId)
    console.log(this.loginIsGuest)
  },
  methods: {
    mongoSleep () {
      if (!this.$refs.form.validate()) {
        return
      }
      this.sleep_loading = true
      axios.post(
        'api/demo:mongoSleep',
        {
          seconds: this.sleep_seconds
        }
      ).then(response => {
        this.sleep_loading = false
        var data = response.data
        alert(data.title)
      }).catch(error => {
        this.sleep_loading = null
        var data = error.response.data
        var errorMessage = data.title
        if (data.description) {
          errorMessage += ' : ' + data.description
        }
        alert(errorMessage)
      })
    },
    publishAsyncTask () {
      if (!this.$refs.form.validate()) {
        return
      }
      this.task_loading = true
      axios.post(
        'api/demo:publishAsyncTask',
        {
          light: this.light_count,
          heavy: this.heavy_count,
        }
      ).then(response => {
        this.task_loading = false
        var data = response.data
        alert(data.title)
      }).catch(error => {
        this.task_loading = null
        var data = error.response.data
        var errorMessage = data.title
        if (data.description) {
          errorMessage += ' : ' + data.description
        }
        alert(errorMessage)
      })
    }
  }
}
</script>
