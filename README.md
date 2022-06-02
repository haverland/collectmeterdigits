## Readout edge AI digits from meters

Help us to get more image data and improve your own digit meter predictions!


### Setup your watermeter device

Before you can read the images, you have to configure the logging of the digits in your device.

Go to you devices and open the configuration.
![Goto Configuration](images/Menu-Config.png)


Now setup the *LogfileRetentionsInDays*. You have to select the checkbox if not already configured.

Please do not change the path of *LogImageLocation* ( /log/digit )

![Setup LogfileRetentionInDays](images/Config-Logimages.png)


If you had to enable the image logging, you need wait a few days before you can readout all the images.


### Read the images

This is mostly the easiest part, if you have installed python on your computer. If not you need to install it ( https://www.python.org/downloads/ ).

Open a terminal and type in:


    pip install git+https://github.com/haverland/collectmeterdigits

    python3 -m collectmeterdigits <your-esp32name> --days=3


It download now all images in a "data" subfolder. The imagenames will be hashed for your privacy. 

After it the duplicates will be automaticly removed and finally you have a zip file with \<your-esp32name\>.zip 

If it is smaller than 2MB you can mail it to iotson(at)t-online.de 

### Comming Next

*  decribe labeling with sample images
*  pre-prediction via tflite

