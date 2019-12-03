import requests
import ftplib
import os

#Allows to upload to the 1fichier account
class FtpUploader:
	
	def __init__(self, host, username, passwordFile, port=21, logging=None):
		if logging:
			self.addLogging(logging)
		#Retrieve password
		with open(passwordFile) as fp:
			password = fp.readline().strip()
		#Enstablish connection
		self.connection = ftplib.FTP_TLS()
		self.connection.connect(host, port)
		if (self.logging): 
			self.logging.info("FtpUploader - uploadFile - Connected to ["+host+"]")
		self.connection.login(username, password)
		if (self.logging): 
			self.logging.info("FtpUploader - uploadFile - Logged as ["+username+"]")
		self.connection.prot_p()
		if (self.logging): 
			self.logging.info("FtpUploader - uploadFile - Connection secured")
	
	#Assign a logging handler
	def addLogging(self, logging):
		self.logging = logging;
		if logging:
			self.logging.info("FtpUploader - Assigned logging handler")
		else:
			print("No logging handler given")
			
	#Upload a file - Return the upload status
	def uploadFile(self, filePath):
		name = os.path.basename(filePath)
		with open(filePath, 'rb') as fp:
			self.connection.storbinary('STOR '+name, fp)
			if (self.logging): 
				self.logging.info("FtpUploader - uploadFile - Uploaded ["+name+"] - ["+filePath+"]")
				print("FtpUploader - uploadFile - Uploaded ["+name+"] - ["+filePath+"]")
			return True;
		return False;
