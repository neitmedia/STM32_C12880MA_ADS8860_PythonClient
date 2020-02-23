# import necessary libs
import serial
import matplotlib.pyplot as plt 
import numpy as np
import sys
from datetime import datetime

# read in command line arguments (integration time, ...)
cmdargs = str(sys.argv)

# set serial port configuration
ser = serial.Serial()
ser.port = '/dev/ttyUSB0' # change this, if you need to use another (virtual) com port
ser.baudrate = 115200 # set baud rate to 115200 baud
ser.timeout = 10 # set serial timeout to 10 seconds
ser.open() # open com port

# if com port is open (no error has occured), start serial communication
if ser.is_open==True:
    # give out status message
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n")
	
	# send new integration time to spectrometer
	bytearr = []
	intTimeMicroseconds = int(sys.argv[1])
	# calculate timer value for spectrometer based on known timing specs
	longInt = round((intTimeMicroseconds-192)/0.033)
	# convert 32 bit int to 4 x 8 bit int
	byte0 = ((longInt >> 24) & 0xFF) ;
	byte1 = ((longInt >> 16) & 0xFF) ;
	byte2 = ((longInt >> 8 ) & 0XFF);
	byte3 = (longInt & 0XFF);
	# control flag
	bytearr.append(0x1F)
	# data bytes
	bytearr.append(byte0)
	bytearr.append(byte1)
	bytearr.append(byte2)
	bytearr.append(byte3)
	# send data
	ser.write(bytearr)
	# don't forget to flush the line, otherwise the spectrometer will not get the data
	ser.write("\r".encode())  	

    # main loop. if data is available, read it
	while 1:
		line = ser.readline();
		try:
            # check if a new spectrum has been read ("!spek!" has been received)
			if ((line[0] == 33) and (line[1] == 115) and (line[2] == 112) and (line[3] == 101) and (line[4] == 107) and (line[5] == 33)):
				spek = []
				# print debug message
				print("neues spektrum!")
				# for every pixel convert the received two 8 bit values to one 16 bit value and save it in the "spek" array
				for i in range(0,288):
					word = ser.read()+ser.read()
					wordint = int.from_bytes(word, byteorder='big', signed=False)
					spek.append(wordint)
                # clear plot
				plt.clf()
				# plot spectrum
				plt.plot(spek)
				# refresh plot
				plt.draw()
				# get current timestamp
				sttime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                # build a string with the current time and the spectrum
				savestring = sttime
				for i in spek:
					savestring = savestring + ',' + str(i)
                # write spectrum to file "spek.log"
				file_object = open('spek.log', 'a')
				file_object.write(savestring+"\n")
				file_object.close()
				
				# wait 1 ms
				plt.pause(0.001)
		except KeyboardInterrupt:
			exit()
