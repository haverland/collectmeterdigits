from urllib.error import HTTPError, URLError
import urllib.request
import re
import requests
import os
from PIL import Image
from datetime import date, timedelta
import imagehash
import secrets
import shutil


target_path = "./data"                   # root data path
target_raw_path =  "./data/raw_images"   # here all raw images will be stored
target_zip_path = "./data/zip_files"

def yesterday(daysbefore=1):
    ''' return the date of yesterday as string in format yyyymmdd'''
    yesterday = date.today() - timedelta(days=daysbefore)
    return yesterday.strftime("%Y%m%d")


def readimages(servername, output_dir, daysback=15):
    '''get all images taken yesterday and store it in target path'''
    serverurl = "http://" + servername
    count = 0
    print(f"Loading data from {servername} ...")
    for datesbefore in range(0, daysback):
        picturedate = yesterday(daysbefore=datesbefore)
        # only if not exists already
        if not os.path.exists(path = output_dir + "/" + servername + "/" + picturedate):
            for i in range(24):
                hour = f'{i:02d}'
                try:
                    fp = urllib.request.urlopen(serverurl + "/fileserver/log/digit/" + picturedate + "/" + hour + "/")
                except HTTPError as h:
                    print( serverurl + "/fileserver/log/digit/" + picturedate + "/" + hour + "/ not found." )
                    continue
                except URLError as ue:
                    print("URL-Error! Server not available? Requested URL was: ", serverurl + "/fileserver/log/digit/" + picturedate + "/" + hour + "/" )
                    exit(1)
                print("Loding ... ",  servername + "/" + picturedate + "/" + hour)
                
                mybytes = fp.read()

                mystr = mybytes.decode("utf8")
                fp.close()

                urls = re.findall(r'href=[\'"]?([^\'" >]+)', mystr)
                path = output_dir + "/" + servername + "/" + picturedate + "/" + hour
                os.makedirs(path, exist_ok=True) 
                for url in urls:
                    prefix = os.path.basename(url).split('_', 1)[0]
                    if (prefix == os.path.basename(url)):
                        prefix = ''
                    else:
                        prefix = prefix + '_'
                    filename = secrets.token_hex(nbytes=16) + ".jpg"
                    if (not os.path.exists(path + "/" + prefix + filename)):
                        
                        img = Image.open(requests.get(serverurl+url, stream=True).raw)
                        img.save(path + "/" + prefix + filename)
                        count = count +1
    print(f"{count} images are loaded from meter: {servername}")



def ziffer_data_files(input_dir):
    '''return a list of all images in given input dir in all subdirectories'''
    imgfiles = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if (file.endswith(".jpg")):
                imgfiles.append(root + "/" + file)
    return  imgfiles

def remove_similar_images(image_filenames, hashfunc = imagehash.average_hash):
    '''removes similar images. 
    
    '''
    images = []
    count = 0
    cutoff = 5  # maximum bits that could be different between the hashes. 
    print(f"Find similar images now in {len(image_filenames)} images ..." )
  
    for img in sorted(image_filenames):
        try:
            hash = hashfunc(Image.open(img).convert('L').resize((32,20)))
        except Exception as e:
            print('Problem:', e, 'with', img)
            continue
        images.append([hash, img])
    
    duplicates = {}
    for hash in images:
        if (hash[1] not in duplicates):
            similarimgs = [i for i in images if abs(i[0]-hash[0]) < cutoff and i[1]!=hash[1]]
            # add duplicates
            if (duplicates == {}):
                duplicates = set([row[1] for row in similarimgs])
            else:
                duplicates |= set([row[1] for row in similarimgs])
            
    print(f"{len(duplicates)} duplicates will be removed.")
    # remove now all duplicates
    for image in duplicates:
        os.remove(image)
        

def create_zip(files, meter):
    print("create a zipfile")
    os.makedirs(target_zip_path, exist_ok=True)
    for file in files:
        os.replace(file, os.path.join(target_zip_path, os.path.basename(file)))
    shutil.make_archive(meter, 'zip', target_zip_path)
       


def collect(meter, days):
    print(meter)
    # ensure the target path exists
    print("retrieve images")
    os.makedirs(target_raw_path, exist_ok=True)
    
    # read all images from meters
    readimages(meter, target_raw_path, days)
    
    # remove all same or similar images and remove the empty folders
    remove_similar_images(ziffer_data_files(os.path.join(target_raw_path, meter)))

    # move the files in one zip without directory structure
    create_zip(ziffer_data_files(os.path.join(target_raw_path, meter)), meter)

    # cleanup
    shutil.rmtree(target_path)


