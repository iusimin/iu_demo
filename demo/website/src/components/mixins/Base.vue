<script>
import {
  mapMutations,
  mapState
} from 'vuex'

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
      axios.get(
        '/api/login',
        {}
      ).then(
        response => {
          var data = response.data
          login.updateLoginStatus(data)
          login.setLoginExpire()
        }
      ).catch(error => { // Login failed
        if (error.response.status === 401) {
          login.updateLoginStatus({
            user_id: null,
            username: null,
            permissions: []
          })
        }
      })
    }
  }
}
</script>
