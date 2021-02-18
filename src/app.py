import bluetooth


#serverMAC = '4C:24:98:D2:19:98'
#port = 3
#s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#s.connect((serverMAC, port))

nearby_devices = bluetooth.discover_devices(duration=20, lookup_names=False,
                                            flush_cache=True, lookup_class=False)
print("Found {} devices.".format(len(nearby_devices)))

a = ''

for addr in nearby_devices:
    print(addr)
    a = addr

services = bluetooth.find_service(address=a)
#services = bluetooth.find_service(address='0C:84:DC:D9:5C:EF')

if len(services) > 0:
    print("Found {} services on {}.".format(len(services), a))
else:
    print("No services found.")

for svc in services:
    print("\nService Name:", svc["name"])
    print("    Host:       ", svc["host"])
    print("    Description:", svc["description"])
    print("    Provided By:", svc["provider"])
    print("    Protocol:   ", svc["protocol"])
    print("    channel/PSM:", svc["port"])
    print("    svc classes:", svc["service-classes"])
    print("    profiles:   ", svc["profiles"])
    print("    service id: ", svc["service-id"])