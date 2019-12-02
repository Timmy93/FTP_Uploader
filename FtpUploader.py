import requests
import ftplib
import os

#Allows to upload to the 1fichier account
class FtpUploader:
	
	def __init__(self, host, username, passwordFile, port):	
		#Retrieve password
		with open(passwordFile) as fp:
			password = fp.readline().strip()
		#Enstablish connection
		self.connection = ftplib.FTP_TLS(host, username, password)
		#Print welcome
		print(self.connection.getwelcome())
	
	def uploadFile(self, filePath):
		filePath = os.path.basename(filePath)
		with open(filePath, 'rb') as fp:
			self.connection.storbinary('STOR '+name, fp)
	
