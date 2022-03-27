import json
from datetime import datetime


data = [1,2,3]
#data = {'another_dict': {'a': 0, 'b': 1}, 'a_list': [0, 1, 2, 3]}
log_file = '../../log/'+(str(datetime.now())[:19].replace(':','-').replace(' ','_'))+'_data.json'  
with open(log_file, 'w') as f: 
    json.dump(data, f)

with open(log_file, 'r') as f:
    a = json.load(f)
print(a)

