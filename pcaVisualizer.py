import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json

def makeAni(virus_dist, antibody_dist):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    ax1.set_title('Virus')
    ax2.set_title('Antibody')

    artists = []
    for data in zip(virus_dist, antibody_dist):
        im_virus = ax1.imshow(data[0], cmap='inferno')
        im_antibody = ax2.imshow(data[1], cmap='viridis')
        artists.append([im_virus, im_antibody])
    
    ani = animation.ArtistAnimation(fig, artists, interval=50)
    plt.show()
    ani.save("./output.gif", writer="pillow")

def makeAniFromJson(pathname):
    infile = open(pathname, "r")

    dist_log = json.load(infile)
    virus_dist = dist_log['virus']
    antibody_dist = dist_log['antibody']

    makeAni(virus_dist, antibody_dist)

    infile.close()

