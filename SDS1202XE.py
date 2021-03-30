import pyvisa
import os
import re
from PIL import Image as PILImage
from IPython.display import Image
from retry import retry

DEBUG = True

# https://siglentna.com/wp-content/uploads/dlm_uploads/2017/10/ProgrammingGuide_forSDS-1-1.pdf

def get_resource_manager():
    return pyvisa.ResourceManager()

def list_resources(rm):
    l = rm.list_resources()
    if len(l) > 0:
        print(l)
    else:
        raise Exception("No VISA device detected.")

def connect(rm, resource):
    sds = rm.open_resource(resource)
    print(sds.query("*IDN?"))
    
    return sds
    

IMG_PATH = "./img"
    
def screenshot(sds, name):
    bmpfile = os.path.join(IMG_PATH, name + ".bmp")
    pngfile = os.path.join(IMG_PATH, name + ".png")
    
    sds.write("SCDP")
    res = sds.read_raw()
    with open(bmpfile, 'wb') as f:
        f.write(res)

    # convert to png
    PILImage.open(bmpfile).save(pngfile)
    os.remove(bmpfile)    
    
    return Image(filename=pngfile) 

#def get_frequency(sds):
#    res = sds.query("CYMOMETER?")
#    print("{}".format(res))

def get_vertical(sds, channel):    
    cmd = "C{}:Volt_DIV?".format(channel)
    res = sds.query(cmd)
    print("{}".format(res))

def set_vertical(sds, channel, volt_by_div):
    cmd = "C{}:VDIV {}".format(channel, volt_by_div)
    sds.write(cmd)

def get_tdiv(sds):
    print(sds.query("TDIV?"))

def set_tdiv(sds, tdiv):
    cmd = "TDIV {}".format(tdiv)
    sds.write(cmd)

def autosetup(sds):
    sds.write("ASET")

def set_phase_measure(sds):
    sds.write("MEAD PHA,C1-C2")

@retry(Exception)
def get_phase(sds):
    res = sds.query("C1-C2:MEAD? PHA")
    # C1-C2:MEAD PHA,-75.72degree
    match = re.search(r"PHA,(.*?)degree", res)
    if match:
        return float(match.group(1))
    else:
        raise Exception("Can't read the phase in {}".format(res))

def set_measure(sds, channel):
    sds.write("PACU PKPK,C{}".format(channel))
    sds.write("PACU FREQ,C{}".format(channel))

@retry(Exception)
def get_measure_vpp(sds, channel):
    res = sds.query("C{}:PAVA? PKPK".format(channel))
    # C1:PAVA PKPK,9.04E+00V
    match = re.search(r"PKPK,(.*?)V", res)
    if match:
        return float(match.group(1))
    else:
        raise Exception("Can't read Peak to Peak value in {}".format(res))

@retry(Exception)
def get_measure_freq(sds, channel):
    res = sds.query("C{}:PAVA? FREQ".format(channel))
    print("{}".format(res))
    
    