import serial.tools.list_ports
import serial

# https://joy-it.net/files/files/Produkte/JT-JD6600/JT-JDS6600-Communication-protocol.pdf

DEBUG = False

def list_com_ports():
    if len(serial.tools.list_ports.comports()) > 0:
        for port in serial.tools.list_ports.comports():
            print("{}".format(port))
    else:
        raise Exception("No serial port detected.")

        
def connect(port):
    return serial.Serial(
        port=port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
    )

SINE = 0
SQUARE = 1
PULSE = 2
TRIANGULAR = 3
    
def set_waveform(serialPort, channel, wave):
    if channel == 1:
        cmd = b'w21'
    else:
        cmd = b'w22'
    # :w21=0.\r\n  sine wave channel 1
    line = b':' + cmd + b'=' + str(wave).encode() + b'.\r\n'
    if DEBUG:
        print("Sending: {}".format(line))
    serialPort.write(line)
    
    res = serialPort.readline()
    if res != b':ok\r\n':
        raise Exception("Can't set waveform {}".format(res))

# frequency in Hz 
def set_frequency(serialPort, channel, frequency):
    if channel == 1:
        cmd = b'w23'
    else:
        cmd = b'w24'
    # :w23=500000,0.\r\n 5KHz channel 1
    line = b':' + cmd + b'=' + str(frequency*100).encode() + b',0.\r\n'
    if DEBUG:
        print("Sending: {}".format(line))
    serialPort.write(line)
    
    res = serialPort.readline()
    if res != b':ok\r\n':
        raise Exception("Can't set frequency {}".format(res))

# amplitude in V
def set_amplitude(serialPort, channel, amplitude):
    if channel == 1:
        cmd = b'w25'
    else:
        cmd = b'w26'
    # :w25=1000.\r\n 1Vpp channel 1
    line = b':' + cmd + b'=' + str(amplitude*1000).encode() + b'.\r\n'
    if DEBUG:
        print("Sending: {}".format(line))
    serialPort.write(line)
    
    res = serialPort.readline()
    if res != b':ok\r\n':
        raise Exception("Can't set amplitude {}".format(res))

# offset in V
# TODO not sure about the calculation!
def set_offset(serialPort, channel, offset):
    if channel == 1:
        cmd = b'w27'
    else:
        cmd = b'w28'
    # :w27=1000.\r\n 0Vpp channel 1
    line = b':' + cmd + b'=' + str(offset*100+1000).encode() + b'.\r\n'
    if DEBUG:
        print("Sending: {}".format(line))
    serialPort.write(line)
    
    res = serialPort.readline()
    if res != b':ok\r\n':
        raise Exception("Can't set amplitude {}".format(res))

def set_output(serialPort, channel1=0, channel2=0):
    line = b':w20=' + str(channel1).encode() + b',' + str(channel2).encode() + b'r\n'
    if DEBUG:
        print("Sending: {}".format(line))
    serialPort.write(line)
    
    res = serialPort.readline()
    if res != b':ok\r\n':
        raise Exception("Can't set output state {}".format(res))
    
   