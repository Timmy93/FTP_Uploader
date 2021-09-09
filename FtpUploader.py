import requests
import ftplib
import os
import time
import sys

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
	#	blocksize	The size of the block to send - Default 256 KiB
	#	maxSpeed	Speed in KB/s to mantain during transfer - Default 0 -> No limit
	def uploadFile(self, filePath, blocksize = 262144, maxSpeed = 0):
		self.writtenSize = 0
		self.maxSpeed = maxSpeed * 1024
		if not self.maxSpeed:
			print("Transferring at maximum speed")
		self.uploadStart = time.time()
		name = os.path.basename(filePath).encode("utf-8", "ignore").decode("latin-1", "ignore")
		with open(filePath, 'rb') as fp:
			try:
				self.connection.storbinary('STOR '+name, fp, blocksize, self.throttler)
				if (self.logging): 
					self.logging.info("FtpUploader - uploadFile - Uploaded ["+name+"] - ["+filePath+"]")
					print("FtpUploader - uploadFile - Uploaded ["+name+"] - ["+filePath+"]")
				return True;
			except ftplib.error_perm:
				self.logging.warn("FtpUploader - uploadFile - Permanent error during upload ["+name+"] - ["+filePath+"]")
			except ftplib.error_temp:
				self.logging.warn("FtpUploader - uploadFile - Temporary error during upload ["+name+"] - ["+filePath+"]")
		return False;
	
	total_length = 0
	start_time = time.time()

	#This function slow down the transmission during
	def throttler(self, buf):
		i = 0
		sleepTime = 0.1
		sleepSeconds = 5
		#Do nothing if no limit set to max speed
		if not self.maxSpeed:
			return
		#Get the written bytes
		self.writtenSize += sys.getsizeof(buf)
		cycles = sleepSeconds/sleepTime
		while self.writtenSize / (time.time() - self.uploadStart) > self.maxSpeed:
			time.sleep(sleepTime)
			i+=1
			if not i%(cycles):
				print("Elapsed: "+str(time.time() - self.uploadStart)+"s, started at "+str(self.uploadStart)+" and written "+str(self.writtenSize/1024/1024)+" MB Sleeping since "+str(sleepSeconds)+" seconds")
	
	#Tries to gracefully exit
	def __del__(self):
		self.connection.quit()
		self.logging.info("FtpUploader - __del__ - Quitted gracefully")
