from loader import *

with open('uid_name_map.json', 'rb') as f:
    uid_name_map = json.loads(f.read())

uid_incomes_counter = {i:0 for i in uid_name_map}

for source_uid, edge_list in json_list.items():
    for edge in edge_list:
        uid_incomes_counter[edge['uid']] += 1
        
uids = set([uid for uid, count in uid_incomes_counter.items() if count >= 2])

with open('graphData_filtered.csv', 'w') as f:
    f.write('source\ttarget\n')

for source_uid, edge_list in json_list.items():
    with open('graphData_filtered.csv', 'a') as f:
        for edge in edge_list:
            if (source_uid in uids) and (edge['uid'] in uids):
                f.write(uid_name_map[source_uid].encode('utf8') + '\t' + edge['nickname'].encode('utf8') + '\n')
