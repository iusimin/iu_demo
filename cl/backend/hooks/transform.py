from datetime import datetime
from bson import ObjectId

def created_ts_to_id(req, resp, resource, params):
    def __convert_ts_to_id(x):
        if isinstance(x, int):
            try:
                dt = datetime.fromtimestamp(x / 1000.0)
                new_x = ObjectId.from_datetime(dt)
            except Exception:
                new_x = x
        elif isinstance(x, dict):
            new_x = {}
            for k, v in x.items():
                new_x[k] = __convert_ts_to_id(v)
        else:
            new_x = x
        return new_x

    def __convert_created_ts_dict(x):
        if isinstance(x, dict):
            new_x = {}
            for k, v in x.items():
                if k == 'created_ts':
                    kval = x.pop(k)
                    new_x['_id'] = __convert_ts_to_id(kval)
                else:
                    new_x[k] = __convert_created_ts_dict(v)
        elif isinstance(x, list):
            new_x = []
            for l in x:
                new_x.append(__convert_created_ts_dict(l))
        else:
            new_x = x
        return new_x
    data = req.context['q']
    if data.get('fields'):
        data['fields'] = [
            f if f != 'created_ts' else '_id' for f in data['fields']]
    if data.get('sort'):
        data['sort'] = [
            t if t[0] != 'created_ts' else ['_id', t[1]]
                for t in data['sort']
        ]
    data['query'] = __convert_created_ts_dict(data['query'])
    req.context['q'] = data

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