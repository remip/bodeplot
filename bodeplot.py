
import matplotlib.pyplot as plt
from scipy import interpolate
from si_prefix import si_format
import numpy as np

def bodeplot(f, g, p, with_fc=False):

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    fig.subplots_adjust(hspace=0.5)
        
    ax1.set_title("Bode plot")

    ax1.set_ylabel('gain (dB)')
    ax1.set_xlabel('f (Hz)')
    ax1.grid(True)
    ax1.semilogx(f, g, 'C2')
    ax1.axhline(y=-3.0)

    if with_fc:
        try:
            # find fc at -3db
            yreduced = np.array(g) - (-3.0)
            freduced = interpolate.UnivariateSpline(f, yreduced, s=0)
            fc = freduced.roots()[0]

            ax1.scatter([fc], [-3.0], c = 'red')
            ax1.annotate("fc=" + si_format(fc, precision=2) + "Hz", xy= (fc, -3.0), xytext=(fc, -2.5) )
        except:
            print("Warning: can't find fc")
    
    ax2.set_ylabel('phase (°)')
    ax2.set_xlabel('f (Hz)')
    ax2.semilogx(f, p, 'C2')
    ax2.grid(True)

    return plt.show()
