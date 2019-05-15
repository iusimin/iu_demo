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
      }
    },
    loginUsername: {
      get () {
        return this.$store.state.login.username
      }
    },
    loginIsGuest: {
      get () {
        return this.$store.state.login.is_guest
      }
    },
    loginPermissions: {
      get () {
        return this.$store.state.login.permissions
      }
    }
  }
}
</script>
