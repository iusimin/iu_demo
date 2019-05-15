import login from '@/utils/login'

export default {
    checkPermissions: function (my_permissions, required_permissions) {
        if (!required_permissions) {
            return true
        }
        for (let r of required_permissions) {
            var matched = my_permissions.some(p => {
                console.log(p.resource + ',' + r.resource)
                var regex = new RegExp(p.resource)
                if (regex.test(r.resource)) {
                    var intersection = r.actions.filter(x => p.actions.includes(x))
                    if (p.actions.length == 0 || intersection.length == r.length) {
                        return p.allow
                    } else {
                        return false
                    }
                }
            })
            if (!matched) {
                // One not match
                return false
            }
        }
        // All match
        return true
    },
    canAccessPage: function(url, router) {
        var matched = router.match(url)
        var res = true
        if (matched.meta.loginRequired) {
            res &= login.hasLoggedIn()
        }
        if (matched.meta.permissionRequired) {
            var my_permissions = login.getLoginData().permissions
            res &= this.checkPermissions(
                my_permissions,
                matched.meta.permissionRequired
            )
        }
        return res
    }
}