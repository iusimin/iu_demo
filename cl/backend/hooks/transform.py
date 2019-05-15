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

def filter_fields(req, resp, resource):
    if not isinstance(resp.media, list):
        return
    ret = []
    if req.method in ['POST', 'PUT', 'PATCH']:
        fields = req.media.get('fields')
    elif req.method in ['GET']:
        fields = req.params.get('fields')
    if not fields:
        return
    for idx, r in enumerate(resp.media):
        if not isinstance(r, dict):
            continue
        new_r = dict(r)
        for k in r:
            if k not in fields:
                new_r.pop(k)
        ret.append(new_r)
    resp.media = ret