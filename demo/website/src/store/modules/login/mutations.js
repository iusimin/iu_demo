import {set} from '@/utils/vuex'

export default {
  setUserId: set('user_id'),
  setUsername: set('username'),
  setIsGuest: set('is_guest'),
  setPermissions: set('permissions')
}
