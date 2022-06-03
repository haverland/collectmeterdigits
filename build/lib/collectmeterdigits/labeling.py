import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider, Button, RadioButtons
from collectmeterdigits.collect import ziffer_data_files
import shutil

def label(path):
    global filename
    global i
    global im
    global filelabel
    global title
    global ax
    global slabel

    files = ziffer_data_files(path)
    i = 0
    filename = files[i]
    img, filelabel = load_image(filename=filename)
    
    title = plt.title(filelabel)  # set title
    plt.xticks([0.2, 0.4, 0.6, 0.8])
    im = plt.imshow(img, aspect='1.6', extent=[0, 1, 0, 1])
    for y in np.arange(0.2, 0.8, 0.2):
        plt.axhline(y=y,color='yellow')
    ax=plt.gca()
    ax.get_xaxis().set_visible(False) 
    #plt.tight_layout()
    axlabel = plt.axes([0.1, 0.025, 0.7, 0.04])
    slabel = Slider(axlabel, label='Label',valmin= 0.1, valmax=9.9, valstep=0.1, 
                    valinit=filelabel,
                    orientation='horizontal')
    nextax = plt.axes([0.87, 0.025, 0.1, 0.04])
    bnext = Button(nextax, 'update', hovercolor='0.975')
    removeax = plt.axes([0.87, 0.4, 0.1, 0.04])
    bremove = Button(removeax, 'delete', hovercolor='0.975')
    
    def load_next():
        global im
        global title
        global slabel
        global i
        global filelabel
        global filename
        
        i = i + 1
        if (i>len(files)-1):
            exit(0)
        filename = files[i]
        img, filelabel = load_image(filename)
        im.set_data(img)
        title.set_text(filelabel)
        slabel.set_val(filelabel)
        plt.draw()

    def remove(event):
        global filename
        os.remove(filename)
        load_next()


    def next(event):
        global filelabel
        global filename
        
        basename = os.path.basename(filename).split('_', 1)
        basename = basename[-1]
        if (filelabel != slabel.val):
            shutil.move(filename, os.path.join(os.path.dirname(filename), str(slabel.val) + "_" + basename))
        load_next()
    
    
    bnext.on_clicked(next)
    bremove.on_clicked(remove)
    plt.show()

    
        


def load_image(filename):
    base = os.path.basename(filename)

    # get label from filename (1.2_ new or 1_ old),
    if (base[1]=="."):
        target = base[0:3]
    else:
        target = base[0:1]
        
    category = float(target)
    
    test_image = Image.open(filename).resize((20, 32))
    return test_image, category
    
