from loader import *

res_dict = {}

for source_uid, edge_list in json_list.items():
    for edge in edge_list:
        nickname = edge['nickname']
        dest_uid = edge['uid']
        res_dict[dest_uid] = nickname
        
with open('uid_name_map.json', 'wb') as f:
    f.write(json.dumps(res_dict))
