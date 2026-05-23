from dataclasses import dataclass
from xml.etree.ElementTree import Element as XMLElement



@dataclass
class Device:
    identifier: str
    id: int
    fwversion: str
    productname: str
    functionbitmask: int
    manufacturer: str

@dataclass
class EnergyMeter(Device):
    # Bit 7
    kWh: float = 0.0
    battery: float = 0.0
    power: float = 0.0

    def parse(self, xml: XMLElement):
        if (battery := xml.find('./battery')) is not None:
            self.battery = float(battery.text)
        if (pm := xml.find('.//powermeter')) is not None:
            self.kWh = int(pm.find('./energy').text) / 1000
            self.power = int(pm.find('./power').text) / 1000

