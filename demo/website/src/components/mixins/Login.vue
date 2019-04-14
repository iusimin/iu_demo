<script>
import {
  mapMutations,
  mapState
} from 'vuex'
import axios from 'axios'
export default {
  computed: {
    ...mapState('login', ['user_id', 'username', 'permissions']),
    loginUserId: {
      get () {
        return this.$store.state.login.user_id
      },
      set (val) {
        this.setUserId(val)
      }
    },
    loginUsername: {
      get () {
        return this.$store.state.login.username
      },
      set (val) {
        this.setUsername(val)
      }
    },
    loginPermissions: {
      get () {
        return this.$store.state.login.permissions
      },
      set (val) {
        this.setPermissions(val)
      }
    }
  },
  methods: {
    ...mapMutations('login', ['setUsername', 'setPermissions', 'setUserId']),
    updateLoginStatus () {
      axios
        .get(
          '/api/login',
          {}
        )
        .then(
          response => {
            var data = response.data
            this.loginPermissions = data.permissions
            this.loginUsername = data.username
            this.loginUserId = data.user_id
          }
        )
        .catch(error => {
          if (error.response.status === 401) {
            this.loginPermissions = []
            this.loginUsername = null
            this.loginUserId = null
          }
        })
    }
  }
}
</script>
