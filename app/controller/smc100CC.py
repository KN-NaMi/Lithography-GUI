import serial
import time
from serial import SerialException
import serial.tools.list_ports
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='smc100.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.DEBUG)

#linkacz do manuala
#https://www.newport.com/medias/sys_master/images/images/h8d/h3a/8797263101982/SMC100CC-SMC100PP-User-Manual.pdf

#linkacz do repo ziomka
#https://github.com/jieunboy0516/Newport-SMC100-Motor-Controller-Library---Python/blob/main/smc100_base.py
state_map=\
	{'0A': 'NOT REFERENCED from reset',
	'0B': 'NOT REFERENCED from HOMING',
	'0C': 'NOT REFERENCED from CONFIGURATION',
	'0D': 'NOT REFERENCED from DISABLE',
	'0E': 'NOT REFERENCED from READY',
	'0F': 'NOT REFERENCED from MOVING',
	'10': 'NOT REFERENCED ESP stage error',
	'11': 'NOT REFERENCED from JOGGING',
	'14': 'CONFIGURATION',
	'1E': 'HOMING commanded from RS-232-C',
	'1F': 'HOMING commanded by SMC-RC',
	'28': 'MOVING',
	'32': 'READY from HOMING',
	'33': 'READY from MOVING',
	'34': 'READY from DISABLE',
	'35': 'READY from JOGGING',
	'3C': 'DISABLE from READY',
	'3D': 'DISABLE from MOVING',
	'3E': 'DISABLE from JOGGING',
	'46': 'JOGGING from READY',
	'47': 'JOGGING from DISABLE',
	'48': 'SIMULATION MODE'}

class smc100:
    def __init__(self, COM=None, devices=2):
        self.serial = serial.Serial()
        self.serial.port = COM
        self.serial.baudrate = 57600
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.devices = []
        self.states=[None]

        try:
            self.serial.open()
        except SerialException:
            return

        self._detect_devices(devices)
        print(self.devices)

    def get_state(self, devices):
        try:
            s=self.send_rcv("01TS")
            device_state=state_map[s[-2:]]
            self.state.states[devices-1]=device_state
            print (device_state)
            return device_state
        except KeyError:
            return 'Strange Error'
            
        
    def _detect_devices(self, max_devices):
        self.send(f'01TS')
        for device_id in range(1, max_devices+1):
            self.send(f'{device_id:02d}OR')
            self.devices.append(f"{device_id:02d}")
                 
    def send(self, command):
       if command[2:] or command[1:] in self.devices:
        self.serial.write((command+'\r\n').encode())
       else:
           logger.error("No such device")

    def kill (self):
        self.serial.close()

    def send_rcv(self, command):
        if command[2:] or command[1:] in self.devices:
            self.serial.write((command+'\r\n').encode())
            return_value=self.serial.readline()
            return return_value[len(command):].strip()
        else:
           logger.error("No such device")

    def move_relative(self, controller, position):
        self.send(f'{controller:02d}PR{position:f}')
    
    def move_absolute(self, controller, position):
        self.send(f'{controller:02d}PA{position:f}')

    def get_pos(self):
        state = self.send_rcv("01TP")
        pos1 = self.send_rcv("01TP")
        state2 = self.send_rcv("02TP")
        pos2 = self.send_rcv("02TP")

        print(f'1{pos1} 2{pos2}')


    def reset(self):
        self.send('01RS')


    
c = smc100("COM4")
c.move_absolute(1,5)
c.move_absolute(2,10)
#c.get_state(1)
#logger.error("No such device")
# ports = serial.tools.list_ports.comports()
# c.move_absolute(1,1)
# c.move_absolute(2,2)
# time.sleep(1)
# c.get_pos()
#c.send_rcv('02OR')
#c.send('01OR')
# c.move_absolute(1, -10)
# c.move_absolute(1,0)
# while True:
#     x = int(input("x= "))
#     c.move_relative(1, x)
#     c.move_relative(2, x)
    # c.move_relative(1, -1)
    # c.move_relative(2, -1)
    # time.sleep(1)
    # c.move_absolute(1, 20)
    # c.move_absolute(2, 20)

# if ports:

#     for port in ports:
#         print(port.device)
# else:
#     print("aha")

    
