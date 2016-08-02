from loader import *

with open('uid_name_map.json', 'rb') as f:
    uid_name_map = json.loads(f.read())

uid2uid_edges = {i:set([edge['uid'] for edge in edge_list]) for i, edge_list in json_list.items()}

with open('graphData_undirected.csv', 'w') as f:
    f.write('source\ttarget\n')
    
for uid1 in uid_name_map:
    if uid1 not in uid2uid_edges: continue
    with open('graphData_undirected.csv', 'a') as f:
        for uid2 in uid_name_map:
            if uid2 not in uid2uid_edges: continue
            if (uid2 in uid2uid_edges[uid1]) and (uid1 in uid2uid_edges[uid2]):
                f.write(uid_name_map[uid1].encode('utf8') + '\t' + uid_name_map[uid2].encode('utf8') + '\n')
                f.write(uid_name_map[uid2].encode('utf8') + '\t' + uid_name_map[uid1].encode('utf8') + '\n')