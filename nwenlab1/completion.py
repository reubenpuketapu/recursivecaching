'''
Created on 14/04/2015

@author: reubenpuketapu
'''

import urllib.request
import re
import os

def pywget(url):
    try: 
        
        direct = url.replace(url.split('/')[-1], "")
        
        with urllib.request.urlopen(url) as response:
            
            data = response.read()  # a `bytes` object
            
            # rewrites the html code to have local file locations
            ahref_files = re.findall(r'<a href="' + direct + '(.*?)"', str(data))
            for link in ahref_files:
                
                if(isinstance(link, str)):
                    data = data.decode("utf-8")
                    data = data.replace(direct + link, link.split('/')[-1])
                    data = data.encode("utf-8")
                    
            # creates all the a href files
            ahref_dir = re.findall(r'<a href="' + '(.*?)"', str(data))
            for link in ahref_dir:
                
                try:
                    with urllib.request.urlopen(direct + link) as response:
                        ahref_data = response.read()
                        makeFile((direct + link).split('/')[-1], ahref_data)
                except Exception as e:
                    print(str(e))
            
            # creates all the img files
            img_files = re.findall(r'<img src="(.*?)">', str(data))
            
            for img_link in img_files:
                if not os.path.exists(img_link.split('/')[0]):
                    os.makedirs(img_link.split('/')[0])
                print(img_link)
                try:
                    with urllib.request.urlopen(direct + img_link) as response:
                        img_data = response.read()
                        makeFile(img_link, img_data)
                        print(img_link)
                except Exception as e:
                    print(str(e))
                    
            # creates index file
            makeFile(url.split('/')[-1], data)
            
    except Exception as e:
        print(str(e))

def makeFile(file_name, data):
    
    filenames = os.listdir(os.curdir)
    file_split = file_name.split('.')
    # finds the highest index of the collisions
    count = 0
    for file in filenames:
        
        if file.startswith(file_split[0]) and file.endswith(file_split[-1]):
            file = str(file).split('.')   
            
            if file[1].isdigit() and int(file[1]) > count:
                
                count = int(file[1])
                
    # makes the file if there is many collisions       
    if not count == 0:
        out_file = open(file_split[0] + '.' + str(count + 1) + '.' + file_split[-1] , 'wb')
        out_file.write(data)
        
    # makes the file if there is only one collision
    elif any(file == file_name for file in filenames):
        out_file = open(file_split[0] + '.1.' + file_split[-1] , 'wb')
        out_file.write(data)
        
    # makes the file if there is no collision
    else:
        out_file = open(file_name, 'wb')
        out_file.write(data)
    
