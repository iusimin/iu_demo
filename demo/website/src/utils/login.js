import store from '@/store'

export default {
    updateLoginStatus: function (data) {
        store.commit('login/setUserId', data.user_id)
        store.commit('login/setUsername', data.username)
        store.commit('login/setPermissions', data.permissions)
    },
    setLoginExpire: function () {
        var current_ts = Date.now();
        store.commit('login/setExpire', current_ts + 5 * 60 * 1000)
    },
    loginExpired: function () {
        return !store.state.login.expire || Date.now() > store.state.login.expire
    },
    hasLoggedIn: function () {
        return store.state.login.user_id !== null
    }
}