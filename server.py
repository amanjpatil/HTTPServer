import socket
from config.config import MAX_CONNECTIONS, PORT
from methods import GET_method , HEAD_method , DELETE_method , POST_method, PUT_method
import sys
import uuid
import threading
import time
import datetime
from datetime import timedelta

threadList = []

def handleRequest( clientSocket , clientAddress):

	#check the method here 
	#appropriately call the method from here
	#also handle the timeout here.
	#send the appropriate response.
	#set timeout 
	#clientSocket.settimeout(10000)
	
	port = list(clientAddress)[1]
	ip = list(clientAddress)[0]
	clientSocket.settimeout(3)
	clientSocket.setblocking(0)

	while 1:
		
		try:
			startTime = datetime.datetime.now()
			data = clientSocket.recv(10485760)
			endTime = datetime.datetime.now()
			decodedData = data.decode('ISO-8859-1')
			isBinary = False

			reqHeader = decodedData.split("\r\n\r\n")[0]
			reqLine = reqHeader.split('\r\n')[0]		
			method = reqLine.split(" ")[0]
			head = reqHeader.split('\r\n')[1:]
			d = dict(item.split(":",1) for item in head)
	
			diff = endTime - startTime
			minutes = diff / timedelta(minutes=1)
			if(abs(minutes) > 0.3):
				status_code = 408
				file_name = "408_error.html"
				response = getTimeout()
				connectionSocket.close()
				errorLog(reqHeader,statusCode ,d)
				print("IN timeout")
				print(response)
				return response
			
			if(method == "GET"):	
				resp = GET_method(decodedData)
				clientSocket.sendall(resp.encode('utf-8'))				
			elif method == "HEAD":
				resp= HEAD_method(decodedData)
				clientSocket.sendall(resp.encode('utf-8'))	
			elif(method == "POST"):
				if '.png' in decodedData or '.jpeg' in decodedData or '.jpg' in decodedData:
					isBinary = True	
				resp = POST_method(decodedData, isBinary)
				clientSocket.sendall(resp.encode('utf-8'))			
			elif(method == "PUT"):
				if '.png' in decodedData or '.jpeg' in decodedData or '.jpg' in decodedData:
					isBinary = True	
				resp = PUT_method(decodedData, isBinary)
				clientSocket.sendall(resp.encode('utf-8'))		
			elif(method == "DELETE"):	
				resp = DELETE_method(decodedData)
				
				clientSocket.sendall(resp.encode('utf-8'))		
	
		except BlockingIOError as e :
			clientSocket.close()
			print("Connection closed with {}".format(clientAddress)) 
			return
		
if __name__ == "__main__":

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('', PORT))

	s.listen(MAX_CONNECTIONS) 
	
	print("Listening on port {}".format(PORT))

	while 1 :
		if len(threadList) < MAX_CONNECTIONS :
			try :
				clientSocket, clientAddress = s.accept()
				newThread = threading.Thread(target=handleRequest, args=[clientSocket, clientAddress], daemon=True)
				threadList.append(newThread)
				newThread.start()
				newThread.join()
				threadList.remove(newThread)
				print('Connection from {}'.format(clientAddress))
			except :
				break