def add_list_index(req, resp, resource):
    if not isinstance(resp.media, list):
        return
    ret = []
    for idx, r in enumerate(resp.media):
        if not isinstance(r, dict):
            ret.append({
                '_index': idx,
                'data': r,
            })
        else:
            ret.append({
                '_index': idx,
            })
            ret[idx].update(r)
    resp.media = ret