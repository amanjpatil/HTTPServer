import pathlib

absPath = str(pathlib.Path().absolute())

PORT = 8080

MAX_CONNECTIONS = 20

DOCUMENT_PATH = absPath +'/media'

NOT_FOUND = absPath + '/media/NOtfound.html'

RESOURCE =  absPath +'/resources/'

CSVPATH = absPath+'/file1.csv'

SAVESUCCESS = absPath +'/media/savesuccessful.html'

UPDATESUCCESS =  absPath +'/media/UPDATESUCCESS.html'

ACCESS_LOG_PATH =  absPath + '/config/access.log'

ERROR_LOG_PATH =  absPath + '/config/error.log'

COOKIE_PATH =  absPath + '/config/Cookie.csv'

ACCESS_DENIED = absPath + '/media/Access_deniedFile.html'

MEDIA_NOT_SUPPORTED = absPath +   '/media/not_supported.html'


#Log format = hostip - [date/month/year hr:min:sec -timezone] "request filename HTTP/1.1" responsecode filelength


