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
            if (error.response) {
                if (errorCallback) {
                    errorCallback(error.response.data);
                } else {
                    new noty({
                        text: error.response.data.msg,
                        type: "error"
                    }).show();
                    //log.error(error.response.data)
                }
            } else {
                console.log(error);
                //log.error(error)
            }
        });
};

export default {
    buildQueryString: function (param_dict) {
        var esc = encodeURIComponent;
        return Object.keys(param_dict)
            .map(k => esc(k) + '=' + esc(param_dict[k]))
            .join('&');
    },
    call: function (method, url, query_string, params, callback, errorCallback, loader) {
        var data = params;
        /* _.pickBy(params, e => {
                   return !_.isNil(e)
               }); */
        //var xsrf_token = $("#xsrf-container").find("input").val();
        var config = {
            data: data,
            method: method,
            url: 'api/' + url,
            headers: {
                //'X-XSRFToken': xsrf_token
            }
        };
        _axios_call(config, callback, errorCallback, loader);
    },
    login: function (username, password, remember_me, callback, errorCallback) {
        this.call(
            "post",
            "login",
            null, {
                username: username,
                password: password
            },
            callback,
            errorCallback
        );
    },
    checkLogin: function (callback, errorCallback) {
        this.call(
            "get",
            "login",
            null,
            null,
            callback,
            errorCallback
        );
    },
    inboundParcel: function (parcel, callback, errorCallback) {
        this.call(
            "put",
            "inbound-parcel/inbound",
            null,
            parcel,
            callback,
            errorCallback
        );
    },
    getParcelSortInfo: function (tracking_id, job_id, round_id, callback, errorCallback) {
        this.call(
            "get",
            "sort_info",
            this.buildQueryString({
                tracking_id: tracking_id,
                job_id: job_id,
                round_id: round_id
            }),
            null,
            callback,
            errorCallback
        );
    }

};