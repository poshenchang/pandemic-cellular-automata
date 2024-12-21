import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
import os

def makePic(virus_dist, antibody_dist, interval=50):
    os.makedirs("./heatmap-images", exist_ok=True)
    for i in range(0, len(virus_dist), interval):
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        ax1.set_title('Virus')
        ax2.set_title('Antibody')
        im_virus = ax1.imshow(virus_dist[i], vmin=0, vmax=0.05, cmap='inferno')
        im_antibody = ax2.imshow(antibody_dist[i], vmin=0, vmax=0.5, cmap='viridis')
        bar1 = plt.colorbar(im_virus)
        bar1.set_label("Virus value") 
        bar2 = plt.colorbar(im_antibody)
        bar2.set_label("Antibody value")
        plt.savefig("./heatmap-images/day" + str(i) + ".png")

def makeSinglePic(dist, interval=50):
    num_figs = len(dist) / interval
    width = int(np.ceil(np.sqrt(num_figs / 1.5)))
    height = int(np.ceil(num_figs / width))
    os.makedirs("./heatmap-images", exist_ok=True)
    fig = plt.figure()
    fig.set_size_inches(12, 15)
    for i in range(0, len(dist), interval):
        ax = fig.add_subplot(height, width, (i//interval)+1)
        # ax.set_title('Virus')
        im_dist = ax.imshow(dist[i], vmin=0, vmax=0.05, cmap='inferno')
        bar = plt.colorbar(im_dist)
        # bar.set_label("Virus value")
    plt.savefig("./heatmap-images/aggregatePic.png")

def makeAni(virus_dist, antibody_dist):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    ax1.set_title('Virus')
    ax2.set_title('Antibody')

    artists = []
    for data in zip(virus_dist, antibody_dist):
        im_virus = ax1.imshow(data[0], vmin=0, vmax=0.05, cmap='inferno')
        im_antibody = ax2.imshow(data[1], vmin=0, vmax=0.5, cmap='viridis')
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

