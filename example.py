#from  utils import responseHeader ,entityHeader
#import csv 

import os 
import signal
import time
#from utils import responseHeader , entityHeader ,statusCodes
#from helper import getDate , getResponse  , getEntity
#import os
#from config.config import DOCUMENT_PATH  , NOT_FOUND
#import sys
#def GET_method(data):
#	#write access log here
#	status_code = ""
#	content_range = 0 
#	l = data.split("\r\n\r\n")
#	reqHeader = l[0]
#	#print("header:")
#	#print(reqHeader)
#	mes = l[1]
#	#print("message is "+ mes)
#	reqLine = reqHeader.split('\r\n')[0]
#	head = reqHeader.split('\r\n')[1:]
#	d = dict(item.split(":",1) for item in head)
#	for i in d :
#		if i == 'Range':
#			new_value = d[i][1:]
#		else: 
#			new_value = d[i][1:]
#			
#		d[i] = new_value
#		
#		
#	#taking path from config and request
#	path = reqLine.split(" ")[1]
#	if path == '/':
#		path = '/index.html'
#		
#	path = DOCUMENT_PATH + path 
#	
#	try :
#		with open(path) as f_obj:
#			print(path)
#	#first check Ranges
#	#if present then it is partial get request and then check If - Ranges in header 
#		#if present then check its value with etag if both are same then not modified status code 206
#		#if both are not matched then dioc is modified  send status code 200
#	#else check if match  in header 
#		#if vaLUE OF IF MATCH IS EQUAL TO ETAG THEN SEND  206 
#		#else send 412 
#			if "Range" in d.keys():
#				#partial get request
#				if "If-Range" in d.keys():
#					
#					if d["If-Range"] ==  "asdfasdfasdfasdfasd" :
#						content_range = d["Range"]
#						print(content_range)
#						status_code = "206"
#					else:
#						status_code = "200"
#				else:
#					if d["If-Match"] == "asdfasdfasdfasdfasd":
#						content_range = d["Range"]
#						status_code = "206"
#					else :
#						status_code = "412"
#			elif "If-Modified-Since" in d.keys(): 
#				#conditional get request
#				if d["If-Modified-Since"] == "asdfasdfasdfasdfasd" :
#					status_code = "304"
#				else:
#					status_code = "200"
#			else :
#				#first get request
#				status_code = "200" 
#			#response = status_line+general_header+ response_header+ entity_header
#			status_line     = "HTTP/1.1" +" "+ status_code + " " +statusCodes[int(status_code)] + "\r\n"
#			general_header  = "Cache:no-cache\r\n" + "Date:" + getDate()+"\r\n" +"Connection:Keep-Alive\r\n"
#			response_header = getResponse(path)
#			entity_header   =  getEntity(path , status_code , content_range  )
#			response =  status_line+ general_header + response_header + entity_header 
#			#message 
#			file_path = open(path)
#			message = file_path.read()
#			file_path.close()
#			#print(response)
#			return response+"\r\n"+message
#			
#	except FileNotFoundError :
#		status_code     = "404"
#		status_line     = "HTTP/1.1" +" "+ status_code + " " +statusCodes[int(status_code)] + "\r\n"
#		general_header  = "Cache:no-cache\r\n" + "Date:" + getDate()+"\r\n" +"Connection:Keep-Alive\r\n"
#		response_header =""
#		entity_header   =""
#		for i in responseHeader :
#			response_header += i
#			response_header += ":"
#			response_header += str(responseHeader[i])
#			response_header += "\r\n"
#		for i in entityHeader :
#			entity_header += i
#			entity_header += ":"
#			if i == "Content-Length":
#				entity_header += str(os.path.getsize(NOT_FOUND))
#			else:
#				entity_header += str(entityHeader[i])
#			entity_header += "\r\n"
#			#file not found error
#		response =  status_line+ general_header + response_header + entity_header 
#		#print(response)
#		file_path = open(NOT_FOUND)
#		message = file_path.read()
#		file_path.close()
#		return response+"\r\n\r\n"+ message


#def HEAD_method(data):
#	res = GET_method(data )
#	response = res.split("\r\n\r\n")[0]
#	#print(response)
#	return response+"\r\n"+"\r\n"






##helper.py



#from datetime import datetime
#import time
#import os
#import csv
#from utils import responseHeader ,entityHeader



#def getDate():
#	date = datetime.now()
#	curr_time = time.localtime()
#	curr_clock = time.strftime("%H:%M:%S", curr_time)
#	data = str(date) + str(curr_clock)
#	return data



#def getEtag(path):
#	with open('file1.csv','r') as longishfile:
#		reader=csv.reader(longishfile)
#		rows=[r for r in reader]
#		
#	for i in rows :
#		if i[0] == path :#path name: 
#			return i[1]

#def getLastmodified(path):
#	with open('file1.csv','r') as longishfile:
#		reader=csv.reader(longishfile)
#		rows=[r for r in reader]
#		
#	for i in rows :
#		if i[0] == path :#path name: 
#			#print(i[2])
#			return i[2]

#def getResponse(path):
#	response_header = ""
#	print("here in get response:"+path)

#	for i in responseHeader :
#		response_header += i
#		response_header += ":"
#		if i == "ETag":
#			print("here in etags")
#			response_header += getEtag(path)
#		else:
#			response_header += str(responseHeader[i])
#		response_header += "\r\n"
#	
#	return response_header 




#def getEntity( path ,status_code = "200"  , content_range = "0" ):
#	entity_header = ""
#	start = 0 
#	end = 0
#	if status_code == '206':
#		if content_range[0] == '-' :
#			end = int(content_range[1:])
#		elif content_range[-1] == '-':
#			start = int(content_range[: -1])
#		else :
#			start = int(content_range.split("-")[0])
#			end =  int(content_range.split("-")[1])
#	
#	if start ==0  and end == 0:
#		content_range =  os.path.getsize(path) 
#	elif end == 0 :
#		content_range = start 
#	else :
#		content_range = end - start
#		
#	for i in entityHeader:
#		entity_header += i
#		entity_header += ":"
#		if i == "Content-Length":
#			entity_header += str(content_range)
#		elif i == "Last-Modified":
#			entity_header += str(getLastmodified(path))
#		elif i == "Content-Range":
#			entity_header += str(start) + "-" + str(end)
#		else:
#			entity_header += str(entityHeader[i])
#		entity_header += "\r\n"
#	return entity_header 
#	







#try: #trying to open a file in read mode 
#	fo = open("myfile.txt","rt")
#	print("File opened")
#	
#except FileNotFoundError: 
#		print("File does not exist") 
#except: 
#	print("Other error")



#/home/aman/Desktop/CN_PROJECT/media/index.html	sdfawef	11/02/19	GET , HEAD











## importing the pandas library
#import pandas as pd

## reading the csv file
#df = pd.read_csv("AllDetails.csv")

## updating the column value/data
#df['Status'] = df['Status'].replace({'P': 'A'})

## writing into the file
#df.to_csv("AllDetails.csv", index=False)

#print(df)


#file_size = os.path.getsize('/home/darshan/Desktop/AMAN_CN/config')
#print(file_size)

# print(os.access( '/home/aman/Desktop/CN_PROJECT/New Folder/AMAN_CN_FINAL/media/index.html', os.R_OK) )

#def handlerequest() :
    #start timeout for 5 min 
    # 
    # while True :
        #try 
        #  
        #       RECEIVE THE MESSAGE 
        #       Do functions 
        #  
        # 
        # except timout occured:
        #   close connection .
        #   return 

import pathlib
abs_path = str(pathlib.Path().absolute())
print(abs_path)