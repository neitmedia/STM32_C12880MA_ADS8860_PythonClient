import serial
import matplotlib.pyplot as plt 
import numpy as np
import sys
from datetime import datetime

cmdargs = str(sys.argv)

ser = serial.Serial()
ser.port = '/dev/ttyUSB0'
ser.baudrate = 115200
ser.timeout = 10
ser.open()
if ser.is_open==True:
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n")
	
	bytearr = []
	longInt = int(sys.argv[1])
	byte0 = ((longInt >> 24) & 0xFF) ;
	byte1 = ((longInt >> 16) & 0xFF) ;
	byte2 = ((longInt >> 8 ) & 0XFF);
	byte3 = (longInt & 0XFF);
	bytearr.append(0x1F)
	bytearr.append(byte0)
	bytearr.append(byte1)
	bytearr.append(byte2)
	bytearr.append(byte3)
	ser.write(bytearr)
	ser.write("\r".encode())  	

	while 1:
		line = ser.readline();
		try:
			if ((line[0] == 33) and (line[1] == 115) and (line[2] == 112) and (line[3] == 101) and (line[4] == 107) and (line[5] == 33)):
				spek = []
				print("neues spektrum:")
				for i in range(0,288):
					word = ser.read()+ser.read()
					wordint = int.from_bytes(word, byteorder='big', signed=False)
					spek.append(wordint)
				plt.clf()
				plt.plot(spek)
				plt.draw()
				sttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
				savestring = sttime
				for i in spek:
					savestring = savestring + ',' + str(i)
				file_object = open('spek.log', 'a')
				file_object.write(savestring+"\n")
				file_object.close()
				
				
				plt.pause(0.001)
		except KeyboardInterrupt:
			exit()
