import json

res = {}
with open('etcd-changes.txt', 'rb') as f:
    lines = f.readlines()
    key = ''
    size = 0
    marker = False
    for l in lines:
        if marker:
            key_long = l.decode('utf-8').strip()
            key_long = key_long.split('/', 4)
            key = '/'.join(key_long[:-1]
                           ) if len(key_long) > 4 else '/'.join(key_long)
            marker = False
        elif l == bytes([0x50, 0x55, 0x54, 0x0D, 0x0A]):
            if key:
                res[key] = res[key] + size if key in res else size
                key = ''
            marker = True
            size = 0
        else:
            size += len(l)


print(json.dumps(res))
