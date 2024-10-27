import serial
import time
from serial import SerialException
#linkacz do manuala
#https://www.newport.com/medias/sys_master/images/images/h8d/h3a/8797263101982/SMC100CC-SMC100PP-User-Manual.pdf

#linkacz do repo ziomka
#https://github.com/jieunboy0516/Newport-SMC100-Motor-Controller-Library---Python/blob/main/smc100_base.py



class smc100:
    def __init__(self, port):
        self.serial=serial.Serial()
        self.serial.port = port 
        self.serial.baudrate = 57600
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity=serial.PARITY_NONE
        self.serial.stopbits=serial.STOPBITS_ONE
        try:
            self.serial.open()
            print("pradzi")
        except SerialException:
            print("nie pradzi")
    
    def _send(self, command):
        self.serial.write(command)

    def set_pos(self, pos):
        self._send(f" {pos}")
    
    def get_pos(self,pos):
        return pos
    
    def num_of_motors(self,num):
        input(num)
        self.motors = num

    def reset(self):
        return self.send('%02dOR')

    def kill(self):
        self.serial.close()


    
