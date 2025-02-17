import numpy as np
import matplotlib.pyplot as plt

def tink(points,x,y,a,b,c,d):
    """
    Iteratively builds two arrays representing the x,y coordinates of
    the Tinkerbell map.

    Arguments:

    points  - number of iterations and coordinates to generate.
    x,y     - initial x,y coordinate pair.
    a,b,c,d - coefficients for the dynamical system.

    Output:

    xs - numpy array of size (points,)
    ys - numpy array of size (points,)
    """
    xs = np.zeros(points)
    ys = np.zeros(points)
    for i in range(points):
        xp = x
        x = xp*xp - y*y + a*xp + b*y
        y = 2*xp*y + c*xp + d*y
        xs[i] = x
        ys[i] = y
    return xs,ys

def make_plot(pltx, plty, num):
    """
    Generate white-on-black tinkerbell map.
    By default saves image to ./figures
    
    Arguments:
    
    pltx - array of x coordinates.
    plty - array of y coordinates.
    """
    plt.figure(figsize=(16,9),facecolor="black")
    plt.scatter(pltx,plty,s=0.1,c="white")
    plt.axis('off')
    plt.xlim(-1.5,0.9)
    plt.ylim(-1.7,0.7)
    plt.savefig("./figures/tink_"+str(num).zfill(4),
                bbox_inches='tight',
                facecolor="black")
    plt.close()

if __name__ == "__main__":
    a,b,c,d = 0.9,-0.6013,2.0,0.50
    points=20000
    x,y=-0.72,-0.64
    
    pltx,plty = tink(points,x,y,a,b,c,d)
    
    make_plot(pltx,plty,0) # num arg set to 0 to output only 1 image.
