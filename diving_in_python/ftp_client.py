from operator import itemgetter

data = 'ok\npalm.cpu 2.0 1150864247\npalm.cpu 0.5 1150864246\n\n'
data = data.rstrip('\n').split('\n')
if data[0] != 'ok':
    raise ClientError
#    return
res = {}
for i in range(1, len(data)):
    item = data[i].split()
    if not item[0] in res.keys():
        res[item[0]] = []
    res[item[0]].append((int(item[2]), float(item[1])))
for key, val in res.items():
    res[key] = sorted(val, key=itemgetter(0))
print(res)