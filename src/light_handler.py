from bluepy.btle import Scanner, DefaultDelegate, Peripheral

SERVICE_HANDLE = 50


def paramToHexStr(p):
    """
    Turns a integer between 0 and 255into a 2-digit Hex representation.
    e.g. 255 => FF, 0 => 00

    :param p: The parameter to transform to a hex version. Min = 0, Max = 255
    :return: A hex representation of the int parameter. 1-digit-hex-numbers are 0-padded.
    """
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
    """
    Returns a byte array that can be sent to the bulbs with the corresponding white and blue values between 0 and 255.

    :param blue: The blue light brightness from 0 (off) to 255 (full brightness)
    :param white: The white light  brightness from 0 (off) to 255 (full brightness)
    :return: A byte sequence that can be sent to the bluetooth light.
    """
    blue = paramToHexStr(blue)
    white = paramToHexStr(white)

    return bytes.fromhex(f"2800 0000 {blue}{white} 000F 29")


def scan():
    """
    scans the area for Relassy Lights (https://www.amazon.de/-/en/gp/product/B07KKBNNS1/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)

    :return: A list of Light objects found
    """
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(6.0)
    lights = []

    for dev in devices:
        name = dev.getValueText(9)
        if name is not None and "Magic" in name:
            lights.append(Light(name, dev.addr))

    return lights


class Light:
    def __init__(self, name, addr):
        self.device = Peripheral(deviceAddr=addr)
        self.name = name
        self.address = addr

    def to_json(self):
        return "{" + f'"name": "{self.name}", "address": "{self.address}"' + "}"

    def to_object(self):
        return {'name': self.name, 'address': self.address}

    def setLight(self, blue, white):
        self.device.writeCharacteristic(SERVICE_HANDLE, getBrightnessCommand(blue, white))

    def getLight(self):
        c = bytes.hex(self.device.readCharacteristic(SERVICE_HANDLE))
        return {'blue': int(c[8:10], 16), 'white': int(c[10:12], 16)}

    def turn_on(self):
        self.device.writeCharacteristic(SERVICE_HANDLE, bytes.fromhex("FBF0 FA"))

    def turn_off(self):
        self.device.writeCharacteristic(SERVICE_HANDLE, bytes.fromhex("FB0F FA"))


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

