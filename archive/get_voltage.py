from ina219 import INA219
import time

SHUNT_OHMS = 0.1
ina = INA219(SHUNT_OHMS)
ina.configure()
print(ina.voltage())