# import serial
# ser = serial.Serial('/dev/tty.usbserial', 9600)
# while 1:
#     ser.readline()


import serial
# from serial.serialutil import SerialException
dev = '/dev/tty.usbmodemfa131'

ser = serial.Serial(dev, 9600, timeout=2)
ser.setRTS(True)
ser.setRTS(False)
while 1:
    try:
        line = ser.readline()
        print(line)
    except Exception, e:
        print e
ser.close
