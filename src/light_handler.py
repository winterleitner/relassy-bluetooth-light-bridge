from bluepy.btle import Scanner, DefaultDelegate, Peripheral

SERVICE_HANDLE = 50


def paramToHexStr(p):
    if p >= 255:
        return "FF"
    if p <= 0:
        return "00"

    h = hex(p)[2:].upper()
    if len(h) == 1:
        return f"0{h}"
    if len(h) == 0:
        return "00"
    return h


def getBrightnessCommand(blue, white):
    blue = paramToHexStr(blue)
    white = paramToHexStr(white)

    return bytes.fromhex(f"2800 0000 {blue}{white} 000F 29")


class Light:
    def __init__(self, name, addr):
        self.name = name
        self.address = addr

    def to_json(self):
        return "{" + f'"name": "{self.name}", "address": "{self.address}"' + "}"

    def to_object(self):
        return {'name': self.name, 'address': self.address}

    def setLight(self, blue, white):
        dev = Peripheral(deviceAddr=self.address)
        dev.writeCharacteristic(SERVICE_HANDLE, getBrightnessCommand(blue, white))

    def getLight(self):
        dev = Peripheral(deviceAddr=self.address)
        c = bytes.hex(dev.readCharacteristic(SERVICE_HANDLE))
        return {'blue': int(c[8:10], 16), 'white': int(c[10:12], 16)}


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)


def scan():
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(4.0)
    lights = []

    for dev in devices:
        name = dev.getValueText(9)
        if name is not None and "Magic" in name:
            lights.append(Light(name, dev.addr))

    return lights


#dev = Peripheral(deviceAddr="4c:24:98:d2:19:98")
#
#s = dev.getServiceByUUID("FFC0")
#for characteristic in s.getCharacteristics():
#    print(characteristic.uuid, characteristic.getHandle())