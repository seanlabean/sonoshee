import numpy as np
from tinker import tink, make_plot

if __name__ == "__main__":
    a,b,c,d = 0.9,-0.6013,2.0,0.50
    x,y=-0.72,-0.64
    points = 20000
    steps = np.arange(-0.5,0.51,0.1)
    num=0
    for step in steps:
        pltx,plty = tink(points,x,y,a,b,c,step)
        make_plot(pltx,plty,num)
        num += 1
