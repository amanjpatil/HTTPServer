from utils import responseHeader , entityHeader ,statusCodes
from helper import getDate , getResponse  , getEntity,getFileNotFoundError , parseURLEncoded , createEtag ,updateEtag , accessLog, setCookie, getExpires ,errorLog,getNotSupported , getAllowedMethods ,getResponseForNotAllowedMethod , getPartialContent , getEtag
import os
from config.config import DOCUMENT_PATH  , NOT_FOUND , RESOURCE ,SAVESUCCESS ,UPDATESUCCESS , ACCESS_DENIED
import sys
import uuid
import json

def GET_method(data):
	status_code = ""
	content_range = 0 
	l = data.split("\r\n\r\n")
	reqHeader = l[0]
	mes = l[1]

	reqLine = reqHeader.split('\r\n')[0]
	head = reqHeader.split('\r\n')[1:]
	d = dict(item.split(":",1) for item in head)
	for i in d :
		if i == 'Range':
			new_value = d[i][1:]
		else: 
			new_value = d[i][1:]
			
		d[i] = new_value		

	#taking path from config and request
	path = reqLine.split(" ")[1]
	if path == '/':
		path = '/index.html'	
	path = DOCUMENT_PATH + path 

	flg = 0
	if 'Cookie' in d and d['Cookie'] != '':
		flg = 1
	cookie = setCookie(flg , d['User-Agent'])
	
	if os.path.exists(path) :
		allowedMethods = getAllowedMethods(path)
		
		if 'GET' in allowedMethods:
			with open(path) as f_obj:
				if "Range" in d.keys():
					#partial get request
					if "If-Range" in d.keys():
						if d["If-Range"] ==  getEtag(path) :
							content_range = d["Range"]
							print(content_range)
							status_code = "206"
							message = getPartialContent(path , content_range) 
						else:
							status_code = "200"
					else:
						if d["If-Match"] == getEtag(path):
							content_range = d["Range"]
							status_code = "206"
							message = getPartialContent(path , content_range) 

						else :
							status_code = "412"
							message = ''

				elif "If-Modified-Since" in d.keys(): 
					#conditional get request
					if d["If-Modified-Since"] ==  getEtag(path) :
						status_code = "304"
						message = ""
					else:
						status_code = "200"
				else :
					#first get request
					status_code = "200" 
				
				#response = status_line+general_header+ response_header+ entity_header
				status_line     = "HTTP/1.1" +" "+ status_code + " " +statusCodes[int(status_code)] + "\r\n"
				general_header  = "Cache:no-cache\r\n" + "Date:" + getDate()+"\r\n" +"Connection:Keep-Alive\r\n"
				response_header = getResponse(path)
				#response header for Set Cookie
				response_header +=  'Set-Cookie' 
				response_header += ':'
				response_header += cookie 
				response_header += 'Expires: '
				response_header += getExpires()
				response_header += "\r\n"
				#entity header
				entity_header   =  getEntity(path , status_code , content_range)
				response =  status_line+ general_header + response_header + entity_header 
				#message 
				if status_code == '200' :
					file_path = open(path)
					message = file_path.read()
					file_path.close()

				accessLog(reqHeader,status_code ,d, path)
				return response+"\r\n"+ message
			
		else:
			#if method for  requested file is not allowed
			response = getResponseForNotAllowedMethod(allowedMethods)
			status_code = '405'
			file_path = open(ACCESS_DENIED)
			message = file_path.read()
			file_path.close()
			errorLog(reqHeader,status_code,d,ACCESS_DENIED)
			return  response + "\r\n" + message
				
	else :
		#if requested file is not present on server
		status_code = '404'
		errorLog(reqHeader,status_code,d,NOT_FOUND)
		return getFileNotFoundError(path)

def HEAD_method(data):
	res = GET_method(data )
	response = res.split("\r\n\r\n")[0]
	return response+"\r\n"+"\r\n"
	
def DELETE_method(data):
	#The DELETE method requests that the origin server delete the resource identified by the Request-URI. 
	#A successful response SHOULD be 200 (OK) if the response includes an entity describing the status, 
	#202 (Accepted) if the action has not yet been enacted
	#or 204 (No Content) if the action has been enacted but the response does not include an entity. 	
	l = data.split("\r\n\r\n")
	reqHeader = l[0]
	mes = l[1]
	reqLine = reqHeader.split('\r\n')[0]
	head = reqHeader.split('\r\n')[1:]
	d = dict(item.split(":",1) for item in head)

	#taking path from config and request
	path = reqLine.split(" ")[1]
	if path == '/':
		path = '/index.html'
	path = DOCUMENT_PATH + path 
	print(path)

	if os.path.exists(path) :
			# fo = open(path,"r")
			# fo.close()
		allowedMethods = getAllowedMethods(path)	
		if 'DELETE' in allowedMethods :
			#remoce data from csv 
			status_code     = "204"
			status_line     = "HTTP/1.1" +" "+ status_code + " " +statusCodes[int(status_code)] + "\r\n"
			entity_header = ""
			general_header  = "Cache:no-cache\r\n" + "Date:" + getDate()+"\r\n" +"Connection:Keep-Alive\r\n"
			#response header
			response_header = getResponse(path)
			#entity header 
			for i in entityHeader :
				entity_header += i
				entity_header += ":"
				entity_header += str(entityHeader[i])
				entity_header += "\r\n"
		
			response = status_line+ general_header + response_header + entity_header

			accessLog(reqHeader,status_code ,d , path)
			os.remove(path)
			return response+"\r\n"
		else :
			response = getResponseForNotAllowedMethod(allowedMethods)
			status_code = '405'
			file_path = open(ACCESS_DENIED)
			message = file_path.read()
			file_path.close()
			errorLog(reqHeader,status_code,d,ACCESS_DENIED)
			return  response + "\r\n" + message

	else :
		status_code = '404'
		errorLog(reqHeader,status_code,d,NOT_FOUND)
		return getFileNotFoundError(path)

#Get the post request
#parse the data according to the content type given in the request.
#if content type is not from the two that we have then the status code is 415.
#create the path from the resource + resource_id 
#extracted data is to be stored in the path formed above in the form of json file

def POST_method(data , isBinary):

	status_code =''
	l = data.split("\r\n\r\n")
	reqHeader = l[0]
	mes = l[1]
	reqLine = reqHeader.split('\r\n')[0]
	head = reqHeader.split('\r\n')[1:]
	d = dict(item.split(":",1) for item in head)
	entity_data = {}

	#taking path from config and request
	path = reqLine.split(" ")[1]
	


	#create the new path for the request.
	uniqueId = str(uuid.uuid1())
	filePath = ""
	
	if(isBinary):
		filePath = RESOURCE +uniqueId +"/"
		os.mkdir(filePath) 
	else :
		filePath = RESOURCE + uniqueId +".json"
	
	#check if the content-type is application/x-www-form-urlencoded 
	#parse the data and convert into the json format and then dump it into the output file.
	if( d['Content-Type'] == " application/x-www-form-urlencoded"): 
		status_code = '201'
		#this method returned the data in json format
		dataToBeWritten = parseURLEncoded(mes)

		#write into the json file
		with open(filePath, "w") as outfile:
			accessLog(reqHeader,status_code ,d , filePath)
			outfile.write(dataToBeWritten)
    			
	elif "multipart/form-data" in d['Content-Type']:
		status_code = '201'
		tempData = data
		boundryLine = d['Content-Type'].split('boundary=')[1]
		fields = tempData.split('--' + boundryLine )
		
		for field in fields[1:]:
			f = field.split('\r\n\r\n')
			if(len(f) ==  1  ):
		  		break 
			value = f[1]

			if 'Content-Type' not in f[0]:
				fieldName = f[0].split('name=')[1]
				entity_data[fieldName] = value
			else :
				
				attributes = f[0].split('\r\n')[1]
			
				fileName = attributes.split('filename=')[1]
				
				fileName = fileName.replace('"', ' ')
				fileName = filePath + fileName 
				
				with open(fileName, "wb") as outfile:
					
					outfile.write(value.encode("ISO-8859-1"))
					
		if len(entity_data) !=  0: 
			json_data = json.dumps(entity_data)
			file_path = filePath + "info.json"
			with open(file_path, "w") as outfile:
				outfile.write(json_data)
				
		accessLog(reqHeader,status_code ,d , filePath)
				
	else :
		status_code ="415"
		errorLog(reqHeader,status_code,d,MEDIA_NOT_SUPPORTED)
		return getNotSupported()
		
	if(status_code != '415'):
		createEtag(filePath)
		file_path = open(SAVESUCCESS)
		message = file_path.read()
		file_path.close()
	
	status_line     = "HTTP/1.1" +" "+ status_code + " " +statusCodes[int(status_code)] + "\r\n"
	entity_header = ""
	general_header  = "Cache:no-cache\r\n" + "Date:" + getDate()+"\r\n" +"Connection:Keep-Alive\r\n"

	response_header = getResponse(filePath)

	for i in entityHeader :
		entity_header += i
		entity_header += ":"
		if i == "Content-Length":
			entity_header += str(os.path.getsize(SAVESUCCESS))
		elif i == "Content-Location" :
			entity_header += filePath
		else:
			entity_header += str(entityHeader[i])
		entity_header += "\r\n"
	response = status_line+ general_header + response_header + entity_header
	
	file_path = open(SAVESUCCESS)
	message = file_path.read()
	file_path.close()
	return response+"\r\n" +message
	
def PUT_method(data , isBinary):
	print("in put method")
	status_code =''
	l = data.split("\r\n\r\n")
	reqHeader = l[0]
	mes = l[1]
	reqLine = reqHeader.split('\r\n')[0]
	head = reqHeader.split('\r\n')[1:]
	d = dict(item.split(":",1) for item in head)
	
	entity_data = {}

	#taking path from config and request
	path = reqLine.split(" ")[1] 

	#check if the path exists
	if os.path.exists(path):
		allowedMethods = getAllowedMethods(path)

		if 'PUT' in allowedMethods:
			status_code = '200'

			#if the given path is file then overwrite the data
			if(os.path.isfile(path)):
				dataToBeWritten = parseURLEncoded(mes)
				with open(path, "w") as outfile:
					accessLog(reqHeader,statusCode ,d , path)
					outfile.write(dataToBeWritten)

			#else open the folder and delete all the existing files and then create new files.
			else:
				for f in os.listdir(path):
	    				os.remove(os.path.join(path, f))
				tempData = data
				boundryLine = d['Content-Type'].split('boundary=')[1]
			
				fields = tempData.split('--' + boundryLine )
		
				for field in fields[1:] :
					f = field.split('\r\n\r\n')
					if(len(f) ==  1  ):
				  		break 
					value = f[1]
					if 'Content-Type' not in f[0]:
						fieldName = f[0].split('name=')[1]
						entity_data[fieldName] = value
					else :
						
						attributes = f[0].split('\r\n')[1]
						
						
						fileName = attributes.split('filename=')[1]
						
						
						fileName = fileName.replace('"', ' ')
						fileName = path + fileName 
						with open(fileName, "wb") as outfile:
							
							outfile.write(value.encode("ISO-8859-1"))
		
				if len(entity_data) !=  0: 
					json_data = json.dumps(entity_data)
					file_path = path + "info.json"
					with open(file_path, "w") as outfile:
						outfile.write(json_data)

				accessLog(reqHeader,statusCode ,d , path)
						
			#first update the etag and create the response
			updateEtag(path)
			
			status_line     = "HTTP/1.1" +" "+ status_code + " " +statusCodes[int(status_code)] + "\r\n"
			entity_header = ""
			general_header  = "Cache:no-cache\r\n" + "Date:" + getDate()+"\r\n" +"Connection:Keep-Alive\r\n"
			response_header = getResponse(path)
			for i in entityHeader :
				entity_header += i
				entity_header += ":"
			
				if i == "Content-Length":
					entity_header += str(os.path.getsize(UPDATESUCCESS))	
				elif i == "Content-Location" :
					entity_header += path	
				else:
					entity_header += str(entityHeader[i])
				entity_header += "\r\n"

			response =  status_line+ general_header + response_header + entity_header
			file_path = open(UPDATESUCCESS)
			message = file_path.read()
			file_path.close()
			
			accessLog(reqHeader,status_code ,d)		

			return response+"\r\n" +message
		else:
			response = getResponseForNotAllowedMethod(allowedMethods)
			status_code = '405'
			file_path = open(ACCESS_DENIED)
			message = file_path.read()
			file_path.close()
			errorLog(reqHeader,status_code,d,ACCESS_DENIED)
			return  response + "\r\n" + message				
	else:
		print("yaa")
		status_code = '201'
		return POST_method(data,isBinary)