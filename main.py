from classes import Room
from cred import ROOMS
from funcs import write_energydb, get_tibber
import time

time.sleep(15)
# 15 Sekunden warten, um API-Sturm zur genauen Viertelstunde zu umgehen

start_time = time.time()

write_energydb("smartmeter", get_tibber())

roomlist = []

for i in ROOMS:
    r = Room(name=i, dbtable=ROOMS[i]["dbtable"], ipaddress=ROOMS[i]["ipaddress"])
    roomlist.append(r)

for ro in roomlist:
    write_energydb(ro.dbtable, ro.consumption)

end_time = time.time()
print(f"Elapsed time: {end_time - start_time:.2f} seconds")