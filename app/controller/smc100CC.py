import serial
import time
from serial import SerialException
import serial.tools.list_ports
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='smc100.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.DEBUG)
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
                all_valid = True
                for device_id in self.devices:
                    state_code = self.send_rcv(f"{device_id}TS").decode()[-2:]
                    print(state_code)
                    state = state_map.get(state_code, "UNKNOWN STATE")
                    
                    if state_code not in valid_states:
                        logger.warning(f"Device {device_id} is in an invalid state: {state}. Cannot perform {func.__name__}.")
                        all_valid = False
                    else:
                        logger.info(f"Device {device_id} is in a valid state ({state}). Proceeding with {func.__name__}")
                if all_valid:
                    return func(self, *args, **kwargs)
                else:
                    logger.error(f"Command {func.__name__} aborted. One or more devices are in invalid states.")
                    return None
            return wrapper
        return decorator

    def get_state(self):
        try:
            for device_id in self.devices:
                state_code=self.send_rcv(f'{device_id:02d}TS').decode()[-2:]
                state = state_map.get(state_code, "UNKNOWN STATE")
                logger.info(f"Device {device_id}: State - {state}")
        except KeyError:    
            logger.debug("Couldn't get state")
            
    
    def _detect_devices(self, max_devices):
        try:
            self.send(f'01TS') 
            for device_id in range(1, max_devices+1):
                self.send(f'{device_id:02d}OR')
                self.devices.append(f"{device_id:02d}")
        except:
            logger.critical("There was a problem detecting your devices")
       
    
    def send(self, command):
       if command[2:] or command[1:] in self.devices:
        self.serial.write((command+'\r\n').encode())
       else:
           logger.error("No such device")

    def send_rcv(self, command):
        if command[2:] or command[1:] in self.devices:
            self.serial.write((command+'\r\n').encode())
            return_value=self.serial.readline()
            return return_value[len(command):].strip()
        else:
           logger.error("No such device")

    @check_state(valid_states=["32","33","34","35"])
    def move_relative(self, controller, position):
        self.send(f'{controller:02d}PR{position:f}')

    @check_state(valid_states=["32","33","34","35"])
    def move_absolute(self, controller, position):
        self.send(f'{controller:02d}PA{position:f}')

    @check_state(valid_states=["32","33","34","35"])
    def get_pos(self):
        for device_id in self.devices:
            pos=self.send_rcv(f'{device_id:02d}TP')
            logger.info(f"Device{device_id} is in {pos} position")

c = smc100("COM3")

c.move_absolute(1, -50)
c.move_absolute(2, -50)
time.sleep(10)
c.move_absolute(1, 50)
time.sleep(3)
c.move_absolute(2, 50)
time.sleep(3)
c.move_absolute(1, -50)
time.sleep(3)
c.move_absolute(2, -50)
time.sleep(3)
c.move_absolute(1, 1)
c.move_absolute(2, 1)
time.sleep(5)
