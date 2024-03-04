import json

res = {}
with open('etcd-changes.txt', 'rb') as f:
    lines = f.readlines()
    key = ''
    size = 0
    marker = False
    for l in lines:
        if marker:
            long = l.decode('utf-8').strip().split('/', 4)
            key = '/'.join(long[:-1]) if len(long) > 4 else '/'.join(long)
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
