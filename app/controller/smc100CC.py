import serial
import time
from serial import SerialException
#test5
class smc100:
    def __init__(self, port):
        self.serial=serial.Serial()
        self.serial.port = port 
        self.serial.baudrate = 57600
        self.serial.bytesize = serial.EIGHTBITS

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
    

    
