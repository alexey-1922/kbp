from pyzabbix import ZabbixAPI
from zabbix_utils import ZabbixAPI
import time
import csv
from operator import itemgetter

#Вариант залогиниться без токена
#z = ZabbixAPI('http://ia-zbx-app1.cdu.so/', user='alyabiev-av', password='PASSWORD')
z = ZabbixAPI('ia-zbx-app1.cdu.so')
z.login(token='723b8c5cc434870037db443019612181ff71e14de3d58e93391c0f60cc15a664')

#Получаем требуемую группу хостов
groups = z.hostgroup.get(output=['itemid','name'])
for group in groups:
    if group['groupid'] == '23':
        name_group = group['name']

#Получаем требуемый хост в группе
hosts = z.host.get(groupids=20, output=['hostid','name'])
for host in hosts:
    if host['hostid'] == '10613':
        name_host = host['name']

#Отбираем требуемые itemid для сбора метрик
items = z.item.get(hostids=10613, output=['itemid','name'], search={'name': 'MSSQL'})
id_linux = {}
for i in (items):
   if '58240' >= i['itemid'] >= '58238':
       key_dict = i['itemid']
       value_dict = i['name']       
       id_linux[key_dict] = value_dict
       
#Интервал снятия метрик ГГГГ,M,DD,H       
time_from = int(time.mktime((2024,3,11,6,0,0,0,0,0)))
time_till = int(time.mktime((2024,3,11,14,0,0,0,0,0)))

#Сбор данных
list_dict = []
cols = ['Time']
for id, name in id_linux.items():   
  cols.append(name)
#Данные возвращаемые с плавающей точкой (history = 0 - numeric float)
  data1 = z.history.get(history = 0, hostids = 10613, itemids = id, time_from=time_from, time_till=time_till)#, limit=3)
#Данные возвращаемые с числовым значением без знака (history = 3 - (default) numeric unsigned)
  data2 = z.history.get(history = 3, hostids = 10613, itemids = id, time_from=time_from, time_till=time_till)#, limit=3)  
#Собираем полученные данные в общий массив [] 
  data3 = data1 + data2 
  
#Создаем словари (data_dict) с искомыми метриками и собираем их в общий массив данных (list_dict)        
  for d in data3:
      data_dict = {}
      time_loc = time.localtime(int(d['clock']))
      time_str_value = time.strftime('%d.%m.%Y %H:%M:%S', time_loc)
      #itemid_value = d['itemid']
      value = d['value']
      #ns_value = d['ns']
      #data_dict['host-name'] = name_host
      #data_dict['groups'] = name_group
      #data_dict['itemid'] = itemid_value
      #data_dict['name'] = name
      data_dict['Time'] = time_str_value
      data_dict[name] = value
      #data_dict['ns'] = ns_value
      #list_dict.append(data_dict)
      list_dict.append(data_dict)

#Сортируем словари в массиве по значению key='Time'
list_dict_sorted = sorted(list_dict, key=itemgetter('Time'))

#Записываем данные из массива list_dict_sorted в файл csv.xlsx, используя лист cols для заголовков таблицы
with open('csv.xlsx', 'w', encoding='utf-8') as f:
     wr = csv.DictWriter(f, fieldnames = cols) 
     wr.writeheader() 
     wr.writerows(list_dict_sorted)
