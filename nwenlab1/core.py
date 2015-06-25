'''
Created on 14/04/2015

@author: reubenpuketapu
'''

import urllib.request
import os

def pywget(url):
    try: 
        with urllib.request.urlopen(url) as response:
            
            file_name = url.split('/')[-1]
            makeFile(url, file_name, response)
            
    except Exception as e:
        print(str(e))
        
def makeFile(url, file_name, response):
    filenames = os.listdir(os.curdir)
    file_split = file_name.split('.')
    #finds the highest index of the collisions
    count = 0
    for file in filenames:
        
        if file.startswith(file_split[0]) and file.endswith(file_split[-1]):
            file = str(file).split('.')   
            
            if file[1].isdigit() and int(file[1]) > count:
                
                count = int(file[1])
                
    #makes the file if there is many collisions       
    if not count == 0:
        out_file = open(file_split[0] + '.' + str(count+1) + '.' + file_split[-1] , 'wb')
        data = response.read()  # a `bytes` object
        out_file.write(data)
        
    #makes the file if there is only one collsion
    elif any(file == url.split('/')[-1] for file in filenames):
        out_file = open(file_split[0] + '.1.' + file_split[-1] , 'wb')
        data = response.read()  # a `bytes` object
        out_file.write(data)
        
    #makes the file if there is no collision
    else:
        out_file = open(url.split('/')[-1], 'wb')
        data = response.read()  # a `bytes` object
        out_file.write(data)

    
