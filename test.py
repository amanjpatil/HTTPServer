from socket import *
import requests
import threading
import sys
import os
import time
from requests.auth import HTTPBasicAuth
from config.config import DOCUMENT_PATH  , NOT_FOUND , RESOURCE ,SAVESUCCESS ,UPDATESUCCESS , ACCESS_DENIED
IP = '127.0.0.1'
port = '8080'
same_url_part = "http://" + IP + ":" + port 

def getRequest() :
    get_Req_1 = requests.get(same_url_part + "/index.html")
    print("GET /index.html: " + str(get_Req_1.status_code)  + str(  get_Req_1.text  )) 
    get_Req_2 = requests.get(same_url_part + "/GET_NOT_ALLOWED.html")
    print("GET /index.html: " + str(get_Req_2.status_code))
    #check 'Range'
    get_Req_3 = requests.get(same_url_part + "/index.html" , headers ={ 'Range' : '-50' , 'If-Range': '2021-10-26 22:34:39.24989522:34:39ce0eaaa9-367e-11ec-82cd-77787e8aa375'}  )
    print("GET /index.html: " + str(get_Req_3.status_code) + str(  get_Req_3.text  ))
    get_Req_4 = requests.get(same_url_part + "/index.html" , headers = {'Range' : '30-60' , 'If-Range' : '2021-10-26 22:34:39.24989522:34:39ce0eaaa9-367e-11ec-82cd-77787e8aa375' } )
    print("GET /index.html: " + str(get_Req_4.status_code) + str(  get_Req_4.text  ))
    get_Req_5 = requests.get(same_url_part + "/index.html" , headers = {'Range' : '150-' , 'If-Range' : '2021-10-26 22:34:39.24989522:34:39ce0eaaa9-367e-11ec-82cd-77787e8aa375'}  )
    print("GET /index.html: " + str(get_Req_5.status_code)   +  str(  get_Req_5.text  ) )
    #check 'Range' for not matched etag
    get_Req_6 = requests.get(same_url_part + "/index.html" , headers = {'Range' : '150-' , 'If-Range' : '2021-10-26 22:00:31.24989522:34:39ce0eaaa9-367e-11ec-82cd-77787e8aa375'}  )
    print("GET /index.html: " + str(get_Req_6.status_code) )


    get_Req_7 = requests.get(same_url_part + "/index.html" ,headers = {'If-Modified-Since' : '2021-10-26 22:34:39.24989522:34:39ce0eaaa9-367e-11ec-82cd-77787e8aa375'}  )
    print("GET /index.html: " + str(get_Req_7.status_code))
    #check if-Modified for not matched etag
    get_Req_8 = requests.get(same_url_part + "/index.html" , headers = {'If-Modified-Since' : '2021-10-26 22:00:32.24989522:34:39ce0eaaa9-367e-11ec-82cd-77787e8aa375'}  )
    print("GET /index.html: " + str(get_Req_8.status_code))


def getHead() :
    get_Req_1 = requests.head(same_url_part + "/index.html")
    print("HEAD /index.html: " + str(get_Req_1.status_code)  + str(  get_Req_1.headers  )) 
    print()
    get_Req_2 = requests.head(same_url_part + "/GET_NOT_ALLOWED.html")
    print("HEAD /index.html: " + str(get_Req_2.status_code) + str(  get_Req_2.headers  ) ) 
    print("")
    #check 'Range'
    get_Req_3 = requests.head(same_url_part + "/index.html" , headers ={ 'Range' : '-50' , 'If-Range': '2021-10-26 22:34:39.24989522:34:39ce0eaaa9-367e-11ec-82cd-77787e8aa375'}  )
    print("HEAD /index.html: " + str(get_Req_3.status_code) + str(  get_Req_3.headers  ))
    get_Req_4 = requests.head(same_url_part + "/index.html" , headers = {'Range' : '30-60' , 'If-Range' : '2021-10-26 22:34:39.24989522:34:39ce0eaaa9-367e-11ec-82cd-77787e8aa375' } )
    print("HEAD /index.html: " + str(get_Req_4.status_code) + str(  get_Req_4.headers  ))
    get_Req_5 = requests.head(same_url_part + "/index.html" , headers = {'Range' : '150-' , 'If-Range' : '2021-10-26 22:34:39.24989522:34:39ce0eaaa9-367e-11ec-82cd-77787e8aa375'}  )
    print("GET /index.html: " + str(get_Req_5.status_code)   +  str(  get_Req_5.headers  ) )
    #check 'Range' for not matched etag
    get_Req_6 = requests.head(same_url_part + "/index.html" , headers = {'Range' : '150-' , 'If-Range' : '2021-10-26 22:00:31.24989522:34:39ce0eaaa9-367e-11ec-82cd-77787e8aa375'}  )
    print("HEAD /index.html: " + str(get_Req_6.status_code) )
    get_Req_7 = requests.head(same_url_part + "/index.html" ,headers = {'If-Modified-Since' : '2021-10-26 22:34:39.24989522:34:39ce0eaaa9-367e-11ec-82cd-77787e8aa375'}  )
    print("HEAD /index.html: " + str(get_Req_7.status_code))
    #check if-Modified for not matched etag
    get_Req_8 = requests.head(same_url_part + "/index.html" , headers = {'If-Modified-Since' : '2021-10-26 22:00:32.24989522:34:39ce0eaaa9-367e-11ec-82cd-77787e8aa375'}  )
    print("HEAD /index.html: " + str(get_Req_8.status_code))

def DeleteMethode() :

    get_Req_1 = requests.delete(same_url_part + "/doDelete.html")
    print("DELETE /doDelete.html: " + str(get_Req_1.status_code)) 
    get_Req_2 = requests.delete(same_url_part + "/doDelete1.html")
    print("DELETE /doDelete.html: " + str(get_Req_2.status_code)) 
    get_Req_3 = requests.delete(same_url_part + "/doDelete2.html")
    print("DELETE /doDelete.html: " + str(get_Req_3.status_code)) 
    get_Req_4 = requests.delete(same_url_part + "/DoDelete_text.txt")
    print("DELETE /doDelete.html: " + str(get_Req_4.status_code))

def postMethod() :
    post_input_1 = {'name':'Aman Patil', 'age':20, 'email':'abc@gmail.com', 'password':'testing', 'gender':'Male', 'game':'Badminton'}
    post_Req_1 = requests.post(same_url_part + "/form.html"   , post_input_1 ) 
    print("POST " + str(post_Req_1.status_code)) 
    
    path = DOCUMENT_PATH +"/dp.jpg"
    with open(path, 'rb') as img:
        name_img= os.path.basename(path) 
        files= {'image': (name_img,img,'multipart/form-data',{'Expires': '0'}) } 
        post_input_2 = {'name':'Aman Patil', 'age':20, 'email':'abc@gmail.com', 'password':'testing', 'gender':'Male', 'game':'Badminton'}
        r = requests.post(same_url_part,files=files ,data = post_input_2 )   
        print( 'POST' + str(r.status_code ))
    
    path = DOCUMENT_PATH +"/dp.jpg"
    with open(path, 'rb') as img:
        name_img= os.path.basename(path) 
        files= {'image': (name_img,img,'multipart/form-data',{'Expires': '0'}) } 
        r = requests.post(same_url_part,files=files)   
        print('POST' + str(r.status_code ))




def putMethod() :

    post_input_1 = {'name':'Aman Patil', 'age':20, 'email':'abc@gmail.com', 'password':'testing', 'gender':'Male', 'game':'Badminton'}
    post_Req_1 = requests.put(same_url_part + "/3b5e5d5e-4595-11ec-94ff-5fb05b379f3d.json"   , post_input_1 ) 
    print("PUT  " + str(post_Req_1.status_code)) 
    
    path = DOCUMENT_PATH +"/dp.jpg"
    with open(path, 'rb') as img:
        name_img= os.path.basename(path) 
        files= {'image': (name_img,img,'multipart/form-data',{'Expires': '0'}) } 
        post_input_2 = {'name':'Aman Patil', 'age':20, 'email':'abc@gmail.com', 'password':'testing', 'gender':'Male', 'game':'Badminton'}
        r = requests.put(same_url_part + '/9f439918-4597-11ec-94ff-5fb05b379f3d',files=files ,data = post_input_2 )   
        print(r.status_code)
    
    path = DOCUMENT_PATH +"/dp.jpg"
    with open(path, 'rb') as img:
        name_img= os.path.basename(path) 
        files= {'image': (name_img,img,'multipart/form-data',{'Expires': '0'}) } 
        r = requests.put(same_url_part + '/6076fc14-4599-11ec-94ff-5fb05b379f3d',files=files)   
        print(r.status_code)


if __name__ == '__main__' :
    # getRequest()
    getRequest()
    DeleteMethode()
    putMethod()
    getHead()
    postMethod()