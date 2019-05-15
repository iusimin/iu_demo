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
      api.checkLogin().then(resp => {
        auth.updateLoginStatus(resp)
        if (resp.is_guest) {
          next({
            path: '/login',
            query: { redirect: to.fullPath }
          });
        } else {
          if (to.matched.some(record => record.meta.requirePermission)) {
            var has_permission = auth.hasPermission(resp, to.fullPath)
            if (!has_permission) {
              // TODO - error page
              alert('403 forbiddened!')
            } else {
              next({
                query: { loginData: resp }
              });
            }
          } else {
            next({
              query: { loginData: resp }
            });
          }
        }
      })
    }
  }
}
</script>
