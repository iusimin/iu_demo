export default {
    generateDatatableQuery: function (data) {
        var query = data.query || {}
        var res = {
            query: query,
            limit: data.pagination.rowsPerPage,
            skip: (data.pagination.page - 1) * data.pagination.rowsPerPage,
            fields: data.headers.filter(h => !h.static).map(h => h.value),
        }
        if (data.pagination.sortBy) {
            res['sort'] = [[
                data.pagination.sortBy,
                data.pagination.descending ? -1 : 1
            ]]
        }
        return res
    }
}