import noty from "noty";
import axios from "axios";

var _axios_call = function (config, callback, errorCallback, loader) {
    if (loader) loader.show();
    axios(config)
        .then(function (resp) {
            if (loader) loader.hide();
            if (callback) callback(resp.data);
        })
        .catch(function (error) {
            if (loader) loader.hide();
            if (error.response && _.isObject(error.response.data)) {
                if (errorCallback) {
                    errorCallback(error.response.data);
                } else {
                    new noty({
                        text: error.response.data.msg,
                        type: "error"
                    }).show();
                    log.error(error.response.data)
                }
            } else {
                log.error(error)
            }
        });
};

export default {
    call_json: function (method, url, params, callback, errorCallback, loader) {
        var data = _.pickBy(params, e => {
            return !_.isNil(e)
        });
        var xsrf_token = $("#xsrf-container").find("input").val();
        var config = {
            data: data,
            method: method,
            url: 'api/' + url,
            headers: {
                'X-XSRFToken': xsrf_token
            }
        };
        _axios_call(config, callback, errorCallback, loader);
    },
    login: function (username, password, remember_me, callback, errorCallback) {
        this.call_json(
            "post",
            "login", {
                username: username,
                password: password,
                remember_me: remember_me
            },
            callback,
            errorCallback
        );
    }
}