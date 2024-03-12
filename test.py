from pyzabbix import ZabbixAPI
import time
import csv

z = ZabbixAPI('http://ia-zbx-app1.cdu.so/', user='alyabiev-av', password='fF}gyu@j~{|i')
#z.login(api_token='e12777f9cf0f1496e6b04a7a69d83587')
#Получаем требуемую группу хостов
groups = z.hostgroup.get(output=['itemid','name'])
for group in groups:
    if group['groupid'] == '20':
        name_group = group['name']

#Получаем требуемый хост в группе
hosts = z.host.get(groupids=20, output=['hostid','name'])
for host in hosts:
    if host['hostid'] == '10605':
        name_host = host['name']


#Получаем список id_linux из id, содержащих в своем наименовании linux
# items = z.item.get(hostids=10605, output=['itemid','name'], search={'name': 'Linux'})
# id_linux = []
# for i in (items):
#   elem = (i['itemid'])       
#   id_linux.append(elem)
#print (id_linux)
items = z.item.get(hostids=10605, output=['itemid','name'], search={'name': 'Linux'})
id_linux = {}
for i in (items):
   key_dict = i['itemid']
   value_dict = i['name']       
   id_linux[key_dict] = value_dict

time_from = int(time.mktime((2024,3,7,9,0,0,0,0,0)))
time_till = int(time.mktime((2024,3,7,13,0,0,0,0,0)))
list_dict = []
#data_dict = {}
for id, name in id_linux.items():
  #list_dict = []  
  data_dict = {}  
  data = z.history.get(history = 0, hostids = 10605, itemids = id, time_from=time_from, time_till=time_till, limit = 10)
  for d in data:
      time_loc = time.localtime(int(d['clock']))
      time_str_value = time.strftime('%d.%m.%Y %H:%M:%S', time_loc)
      itemid_value = d['itemid']
      value = d['value']
      ns_value = d['ns']
      #print('itemid:', itemid_value, 'clock:', time_str_value, 'value:', value, 'ns:', ns_value)
      data_dict['host-name'] = name_host
      data_dict['groups'] = name_group
      data_dict['itemid'] = itemid_value
      data_dict['name'] = name
      data_dict['clock'] = time_str_value
      data_dict['value'] = value
      data_dict['ns'] = ns_value
      list_dict.append(data_dict)
print(list_dict)
cols = ['host-name', 'groups', 'itemid', 'name', 'clock', 'value', 'ns']
with open('csv.xlsx', 'w', encoding='utf-8') as f:
    wr = csv.DictWriter(f, fieldnames = cols) 
    wr.writeheader() 
    wr.writerows(list_dict)
     


