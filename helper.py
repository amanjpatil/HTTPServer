from datetime import *
import time
import os
import csv
from utils import responseHeader ,entityHeader ,statusCodes
from config.config import DOCUMENT_PATH  , NOT_FOUND , CSVPATH, ACCESS_LOG_PATH, COOKIE_PATH , ACCESS_DENIED, MEDIA_NOT_SUPPORTED , ERROR_LOG_PATH
import uuid
import  json
import pandas as pd
from csv import writer

def getDate():
	date = datetime.now()
	curr_time = time.localtime()
	curr_clock = time.strftime("%H:%M:%S", curr_time)
	data = str(date) + str(curr_clock)
	return data

def getEtag(path):
	with open(CSVPATH,'r') as longishfile:
		reader=csv.reader(longishfile)
		rows=[r for r in reader]
	for i in rows :
		if i[0] == path :
			return str(i[1])

def updateEtag(path):
	df = pd.read_csv(CSVPATH)
	oldEtag = getEtag(path)
	date = getDate()
	uniqueId = str(uuid.uuid1())
	newEtag = date + uniqueId
	# updating the column value/data
	#updating the etag
	df['etag'] = df['etag'].replace({ oldEtag : newEtag })
	#updating the lastModified
	oldLastModified = oldEtag[0:34]
	newLastModified = date
	df['lastmodified'] = df['lastmodified'].replace({oldLastModified : newLastModified}) 
	print("Old etag:" + oldEtag + " new Etag:" + newEtag)
	# writing into the file
	df.to_csv( CSVPATH, index=False)
	
def createEtag(path):
	date = getDate()
	uniqueId = str(uuid.uuid1())
	Etag = date+uniqueId
	row = [path , Etag , date ,'GET ,PUT , DELETE']
	# open the file in the write mode
	with open(CSVPATH, 'a') as f_object:
		writer_object = writer(f_object)
    	# Pass the list as an argument into
 		# the writerow()
		writer_object.writerow(row)
    	#Close the file object
		f_object.close()

def getLastmodified(path):
	with open('file1.csv','r') as longishfile:
		reader=csv.reader(longishfile)
		rows=[r for r in reader]	
	for i in rows :
		if i[0] == path :#path name: 
			#print(i[2])
			return i[2]

def getResponse(path):
	response_header = ""
	#print("here in get response:"+path)
	for i in responseHeader :
		response_header += i
		response_header += ":"
		if i == "ETag":
			print("here in etags")
			response_header += getEtag(path)
		else:
			response_header += str(responseHeader[i])
		response_header += "\r\n"
	return response_header 

def getEntity( path ,status_code = "200"  , content_range = "0" ):
	entity_header = ""
	start = 0 
	end = 0
	if status_code == '206':
		if content_range[0] == '-' :
			end = int(content_range[1:])
		elif content_range[-1] == '-':
			start = int(content_range[: -1])
		else :
			start = int(content_range.split("-")[0])
			end =  int(content_range.split("-")[1])
	if start ==0  and end == 0:
		content_range =  os.path.getsize(path) 
	elif end == 0 :
		content_range = start 
	else :
		content_range = end - start
	for i in entityHeader:
		entity_header += i
		entity_header += ":"
		if i == "Content-Length":
			entity_header += str(content_range)
		elif i == "Last-Modified":
			entity_header += str(getLastmodified(path))
		elif i == "Content-Range":
			entity_header += str(start) + "-" + str(end)
		else:
			entity_header += str(entityHeader[i])
		entity_header += "\r\n"
	return entity_header 
	
def getFileNotFoundError(path):
	status_code     = "404"
	status_line     = "HTTP/1.1" +" "+ status_code + " " +statusCodes[int(status_code)] + "\r\n"
	general_header  = "Cache:no-cache\r\n" + "Date:" + getDate()+"\r\n" +"Connection:Keep-Alive\r\n"
	response_header =""
	entity_header   =""
	for i in responseHeader :
		response_header += i
		response_header += ":"
		response_header += str(responseHeader[i])
		response_header += "\r\n"
	for i in entityHeader :
		entity_header += i
		entity_header += ":"
		if i == "Content-Length":
			entity_header += str(os.path.getsize(NOT_FOUND))
		else:
			entity_header += str(entityHeader[i])
		entity_header += "\r\n"
		#file not found error
	response =  status_line+ general_header + response_header + entity_header 
	#print(response)
	file_path = open(NOT_FOUND)
	message = file_path.read()
	file_path.close()
	return response+"\r\n"+ message

def parseURLEncoded(data):
    data = data.split("&")
    parameters = {}
    for param in data:
        divide = param.split("=")
        parameters[str(divide[0])] = divide[1]       
    json_data = json.dumps(parameters)
    return json_data
    
def errorLog( reqHeader, statusCode ,d , fileName = '' ):
	reqLine = reqHeader.split('\r\n')[0]	
	userAgent = d['User-Agent']
	if fileName != '':
		fileLength = os.path.getsize(fileName)
	else :
		fileLength = 0	
	errorLogString = '127.0.0.1 - - [' + getDate() + '] ' + reqLine.split(' ')[0] + ' ' + fileName + ' ' + reqLine.split(' ')[2]  + ' ' + statusCode + ' '+ str(fileLength) + '-' + userAgent + '\n'
	print("in error log")
	print(errorLogString)
	file1 = open(ERROR_LOG_PATH, "a+") 
	file1.write(errorLogString)

#Log format = hostip - [date/month/year hr:min:sec -timezone] "request filename HTTP/1.1" responsecode filelength
def accessLog( reqHeader, statusCode ,d , fileName ):
	reqLine = reqHeader.split('\r\n')[0]	
	userAgent = d['User-Agent']
	fileLength = os.path.getsize(fileName)
	accessLogString = '127.0.0.1 - - [' + getDate() + '] ' + reqLine.split(' ')[0] + ' ' + fileName + ' ' + reqLine.split(' ')[2]  + ' ' + statusCode + ' '+ str(fileLength) + '-' + userAgent + '\n'
	file1 = open(ACCESS_LOG_PATH, "a") 
	file1.write(accessLogString)

def setCookie(  flg , userAgent):
	#find the path and increment the count
	if flg:
		with open(COOKIE_PATH, 'r') as f:
			file = csv.reader(f)
			my_list = list(file)	
		for x in my_list:
			if userAgent in x:
				cookie  = x[1]
				x[2] =  str(int(x[2] )+ 1) 		
		fields = ['User-Agent', 'Cookie', 'Count'] 
		with open(COOKIE_PATH, 'w') as f:
			    write = csv.writer(f)
			    write.writerows(my_list)	
#	add the userAgent and cookie
	else:
		cookie = str(uuid.uuid1())
		List=[ userAgent  , cookie ,  1]
		with open(COOKIE_PATH, 'a') as f_object:
		    writer_object = writer(f_object)
		    writer_object.writerow(List)
		    f_object.close()
	return cookie
	
def getExpires():
	ini_time_for_now = datetime.now()
	new_time = ini_time_for_now  + timedelta(hours = 24)
	return str(new_time)
		
def getAllowedMethods( path ):
	with open(CSVPATH,'r') as longishfile:
		reader=csv.reader(longishfile)
		rows=[r for r in reader]
	for i in rows :
		if i[0] == path :
			temp = []
			string = ""
			for x in i[3] :
				if x == ',' :
					temp.append(string)
					string = ""
				elif x ==" " :
					pass
				else :
					string += x
			temp.append(string)
			return temp

def getResponseForNotAllowedMethod(allowedMethods):
	status_code = '405'	
	status_line     = "HTTP/1.1" +" "+ status_code + " " +statusCodes[int(status_code)] + "\r\n"
	general_header  = "Cache:no-cache\r\n" + "Date:" + getDate()+"\r\n" +"Connection:Keep-Alive\r\n"
	response_header =""
	entity_header   =""
	for i in responseHeader :
		response_header += i
		response_header += ":"
		response_header += str(responseHeader[i])
		response_header += "\r\n"
	for i in entityHeader :
		entity_header += i
		entity_header += ":"
		if i == "Content-Length":
			entity_header += str(os.path.getsize(ACCESS_DENIED))
		elif i == "Allow" :
			for x in allowedMethods :
				entity_header += x
				entity_header += " "
		else:
			entity_header += str(entityHeader[i])
		entity_header += "\r\n"
	response  =  status_line + general_header + response_header + entity_header
	return response
	
def getNotSupported():
	status_code = '415'	
	status_line     = "HTTP/1.1" +" "+ status_code + " " +statusCodes[int(status_code)] + "\r\n"
	general_header  = "Cache:no-cache\r\n" + "Date:" + getDate()+"\r\n" +"Connection:Keep-Alive\r\n"
	response_header =""
	entity_header   =""
	for i in responseHeader :
		response_header += i
		response_header += ":"
		response_header += str(responseHeader[i])
		response_header += "\r\n"
	for i in entityHeader :
		entity_header += i
		entity_header += ":"
		if i == "Content-Length":
			entity_header += str(os.path.getsize(MEDIA_NOT_SUPPORTED))
		else:
			entity_header += str(entityHeader[i])
		entity_header += "\r\n"
	response  =  status_line + general_header + response_header + entity_header
	return response
	
def getTimeout():
	status_code = '408'
	status_line     = "HTTP/1.1" +" "+ status_code + " " +statusCodes[int(status_code)] + "\r\n"
	general_header  = "Cache:no-cache\r\n" + "Date:" + getDate()+"\r\n" +"Connection:Close\r\n"
	response_header =""
	entity_header   =""
	for i in responseHeader :
		response_header += i
		response_header += ":"
		response_header += str(responseHeader[i])
		response_header += "\r\n"
	for i in entityHeader :
		entity_header += i
		entity_header += ":"
		if i == "Content-Length":
			entity_header += '0'
		else:
			entity_header += str(entityHeader[i])
		entity_header += "\r\n"
	response  =  status_line + general_header + response_header + entity_header
	return response

def getPartialContent(path , content_range) :
	file_path = open(path)
	message = file_path.read()
	start = 0 
	end = 0
	if content_range[0] == '-' :
		end = int(content_range[1:])
	elif content_range[-1] == '-':
		start = int(content_range[: -1])
		end = os.path.getsize(path)
	else :
		start = int(content_range.split("-")[0])
		end =  int(content_range.split("-")[1])

	
	file_path.close()

	return message[start : end]