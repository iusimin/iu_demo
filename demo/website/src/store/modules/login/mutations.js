import {set} from '@/utils/vuex'

export default {
  setUsername: set('username'),
  setUserId: set('user_id'),
  setPermissions: set('permissions'),
  setExpire: set('expire')
}
