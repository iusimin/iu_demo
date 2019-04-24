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
        url = 'api/' + url;
        if (query_string) {
            url = url + "?" + query_string
        }
        var config = {
            data: data,
            method: method,
            url: url,
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
    getInboundParcelDetail: function(tracking_id, callback, errorCallback) {
        this.call(
            "get",
            "inbound-parcel/" + tracking_id,
            null,
            null,
            callback,
            errorCallback
        );
    },
    getParcelSortInfo: function (tracking_id, job_id, round_id, callback, errorCallback) {
        this.call(
            "get",
            "sort-info",
            this.buildQueryString({
                tracking_id: tracking_id,
                job_id: job_id,
                round_id: round_id
            }),
            null,
            callback,
            errorCallback
        );
    },
    getSeedCabinet: function (tracking_id, job_id, callback, errorCallback) {
        this.call(
            "get",
            "seed-pool",
            this.buildQueryString({
                tracking_id: tracking_id,
                job_id: job_id
            }),
            null,
            callback,
            errorCallback
        );
    },
    getSortJobs: function (pagination, callback, errorCallback) {
        this.call(
            "post", // post as get
            "sort-jobs",
            null, {
                pagination: pagination
            },
            callback,
            errorCallback
        );
    },
    createNewSortJob: function (job_type, callback, errorCallback) {
        this.call(
            "post",
            "sort-job",
            null,
            {
                job_type: job_type
            },
            callback,
            errorCallback
        );
    },
    getSortJobDetail: function (job_id, callback, errorCallback) {
        this.call(
            "get",
            "sort-job",
            this.buildQueryString({
                job_id: job_id
            }),
            null,
            callback,
            errorCallback
        );
    },
    cancelSortJob: function(job_id, callback, errorCallback) {
        this.call(
            "put",
            "sort-job",
            null,
            {
                job_id: job_id,
                action: "Cancel"
            },
            callback,
            errorCallback
        );
    },
    getActiveSortJob: function(callback, errorCallback) {
        this.call(
            "get",
            "active-sort-job",
            null,
            null,
            callback,
            errorCallback
        );
    }
};