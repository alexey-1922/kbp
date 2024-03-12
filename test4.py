import csv
from operator import itemgetter

l = [{'Time': '11.03.2024 06:00:03', 'MSSQL: Total average wait time': '0'},
     {'Time': '11.03.2024 06:02:03', 'MSSQL: Total average wait time': '0'},
     {'Time': '11.03.2024 06:04:09', "MSSQL: Service's TCP port state": '1'},
     {'Time': '11.03.2024 06:14:09', "MSSQL: Service's TCP port state": '1'},
     {'Time': '11.03.2024 06:24:09', "MSSQL: Service's TCP port state": '1'},
     {'Time': '11.03.2024 06:00:03', 'MSSQL: Average latch wait time': '0.09523809523809523'},
     {'Time': '11.03.2024 06:01:03', 'MSSQL: Average latch wait time': '0.19230769230769232'},
     {'Time': '11.03.2024 06:02:03', 'MSSQL: Average latch wait time': '0.018433179723502304'}
     ]
cols = ['Time', 'MSSQL: Total average wait time', "MSSQL: Service's TCP port state", 'MSSQL: Average latch wait time']


newlist = sorted(l, key=itemgetter('Time')) #reverse=True)
print(newlist)

with open('csv.xlsx', 'w', encoding='utf-8') as f:
     wr = csv.DictWriter(f, fieldnames = cols) 
     wr.writeheader() 
     wr.writerows(newlist)