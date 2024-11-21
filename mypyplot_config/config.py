import colorsys
from typing import Callable, Tuple, Union

import matplotlib
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "DejaVu Serif" 
from cycler import cycler

plt.rcParams['axes.prop_cycle']  = cycler(color=['#FF4B00', '#005AFF', '#03AF7A', '#4DC4FF','#F6AA00',
                                                 '#FFF100','#000000'])

plt.rcParams["font.size"] = 22
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

plt.rcParams["contour.linewidth"] = 1.0


cmap_types = Union[matplotlib.colors.Colormap,
                   Callable[[float], Tuple[float, float, float, float]]]


def tone_correction(cmap: cmap_types,
                    nsamples: int,
                    dh: float,
                    ds: float,
                    dv: float) -> matplotlib.colors.LinearSegmentedColormap:
    """Tone correction to cmap.

    Parameters
    ----------
    cmap : cm.Cmap
        Color map
    nsamples : int

    dh : float
        Hue difference (-1.0 ~ 1.0)
    ds : float
        Saturation difference (-1.0 ~ 1.0)
    dv : float
        Value difference (-1.0 ~ 1.0)

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        [description]
    """
    cdict = {'red': [], 'green': [], 'blue': []}
    for i in range(nsamples):
        loc = i / (nsamples - 1)
        r, g, b, _ = cmap(loc)

        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h = max(0, min(h + dh, 1))
        s = max(0, min(s + ds, 1))
        v = max(0, min(v + dv, 1))

        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        cdict['red'].append((loc, r, r))
        cdict['green'].append((loc, g, g))
        cdict['blue'].append((loc, b, b))

    return matplotlib.colors.LinearSegmentedColormap('cmap', cdict)


_r = 0.9
_d = 0.5
gray_jet = mcolors.LinearSegmentedColormap('gray-jet', {
    'red':   ((0.00, 0.2, 0.2),
              (_d*(1-_r), 0.3, 0.3),
              (0.35*_r+(1-_r), 0, 0),
              (0.66*_r+(1-_r), 1, 1),
              (0.89*_r+(1-_r), 1, 1),
              (1.00, 0.5, 0.5)),
    'green': ((0.00, 0.2, 0.2),
              (_d*(1-_r), 0.3, 0.3),
              (0.125*_r+(1-_r), 0, 0),
              (0.375*_r+(1-_r), 1, 1),
              (0.640*_r+(1-_r), 1, 1),
              (0.910*_r+(1-_r), 0, 0),
              (1.000, 0, 0)),
    'blue':  ((0.00, 0.2, 0.2),
              (_d*(1-_r), 0.3, 0.3),
              (0.00*_r+(1-_r), 0.5, 0.5),
              (0.11*_r+(1-_r), 1, 1),
              (0.34*_r+(1-_r), 1, 1),
              (0.65*_r+(1-_r), 0, 0),
              (1.00, 0, 0))
})

myjet = tone_correction(cm.jet, 20, 0, -0.6, 0.3)
mygray_jet = tone_correction(gray_jet, 20, 0, -0.6, 0.3)
mask_color = '#DDD'

myjet.set_bad(color=mask_color)
mygray_jet.set_bad(color=mask_color)

line_color = '#222'
linewidth = 1.5
