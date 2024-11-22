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

#01TS,02TS - > 01OR, 02OR - > move
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
            self._detect_devices(devices)
        except SerialException:
            logger.critical("Serial not working")



    def check_state(valid_states):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                current_state_code1 = self.send_rcv("01TS").decode()[-2:] 
                current_state_code2 = self.send_rcv("02TS").decode()[-2:] 
                current_state1 = state_map.get(current_state_code1, "UNKNOWN STATE")
                current_state2 = state_map.get(current_state_code2, "UNKNOWN STATE")
                if current_state_code1 or current_state2 in valid_states:
                    logger.info(f"Current state of first controller: {current_state1}. Proceeding with {func.__name__}.")
                    logger.info(f"Current state of second controller: {current_state2}. Proceeding with {func.__name__}.")
                    return func(self, *args, **kwargs)
                else:
                    logger.warning(f"Cannot perform {func.__name__}. Device one is in state: {current_state1}.")
                    logger.warning(f"Cannot perform {func.__name__}. Device two is in state: {current_state2}.")
                    return None 
            return wrapper
        return decorator

    def get_state(self):
        try:
            s=self.send_rcv("01TS")
            s2=s.decode()[-2:]
            device_state=state_map.get(s2)
            print(device_state)
            
        except KeyError:    
            logger.debug("Couldn't get state")
            
    
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

    @check_state(valid_states=["32", "33","34","35"])
    def move_relative(self, controller, position):
        self.send(f'{controller:02d}PR{position:f}')

    @check_state(valid_states=["32", "33","34","35"])
    def move_absolute(self, controller, position):
        self.send(f'{controller:02d}PA{position:f}')

    #do zmiany warunki
    @check_state(valid_states=["32", "33","34","35"])
    def get_pos(self):
        pos1 = self.send_rcv("01TP")
        pos2 = self.send_rcv("02TP")

        print(f'1 {pos1} \n2 {pos2}')

    def reset(self):
        self.send('01RS')


    
c = smc100("COM4")

#trojkat 
# c.move_absolute(1, -50)
# c.move_absolute(2, -50)
# time.sleep(10)
# c.move_absolute(1, 50)
# time.sleep(3)
# c.move_absolute(2, 50)
# time.sleep(3)
# c.move_absolute(1, -50)
# time.sleep(3)
# c.move_absolute(2, -50)
# time.sleep(3)
# c.move_absolute(1, 1)
# c.move_absolute(2, 1)
# time.sleep(5)