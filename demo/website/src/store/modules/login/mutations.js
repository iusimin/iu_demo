import {set} from '@/utils/vuex'

export default {
  setUsername: set('username'),
  setUserId: set('user_id'),
  setPermissions: set('permissions')
  // setDrawer: set('drawer'),
  // setImage: set('image'),
  // setColor: set('color'),
  // toggleDrawer: toggle('drawer')
}
