import requests
import ftplib
import os

#Allows to upload to the 1fichier account
class FtpUploader:
	
	def __init__(self, host, username, passwordFile, port=21):	
		#Retrieve password
		with open(passwordFile) as fp:
			password = fp.readline().strip()
		#Enstablish connection
		self.connection = ftplib.FTP_TLS(source_address=(host, port), username, password)
		#Print welcome
		print(self.connection.getwelcome())
	
	#Assign a logging handler
	def addLogging(self, logging):
		self.logging = logging;
		self.logging.info("FtpUploader - Assigned logging handler")
			
	#Upload a file
	def uploadFile(self, filePath):
		name = os.path.basename(filePath)
		with open(filePath, 'rb') as fp:
			self.connection.storbinary('STOR '+name, fp)
		if (self.logging): 
			self.logging.info("FtpUploader - uploadFile - Uploaded ["+name+"]")
