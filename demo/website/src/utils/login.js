import store from '@/store'

export default {
    updateLoginStatus: function (data) {
        store.commit('login/setIsGuest', data.is_guest)
        store.commit('login/setUserId', data.user_id)
        store.commit('login/setPermissions', data.permissions)
        store.commit('login/setUsername', data.username)
    },
    hasLoggedIn: function () {
        return !store.state.login.is_guest
    },
    getLoginData: function() {
        return store.state.login
    }
}