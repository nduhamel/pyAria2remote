#!/usr/bin/python
import xmlrpclib

from repl import Formater, REPL
from utils import sizeof_fmt, simple_eta, achievepercent

class AriaDownloadFormater(Formater):
	
	def __init__(self, ariadownload):
		assert isinstance(ariadownload, AriaDownload)
		self.download = ariadownload
	
	def pprint(self):		
		status = self.download.status
		status["percent"] = str(achievepercent(int(status["totalLength"]), int(status["completedLength"])))
		restant = int(status["totalLength"]) -  int(status["completedLength"])
		status["ETA"] = str(simple_eta(restant, int(status["speed"]) ))
		status["speed"] = sizeof_fmt(int(status["speed"]))+"/s"
		status["completedLength"]= sizeof_fmt(int(status["completedLength"]))
		status["totalLength"] = sizeof_fmt(int(status["totalLength"]))
		print "-------------------------------------------"
		for (k,v) in status.items():
			print k+":  "+str(v)
		print "-------------------------------------------"

class AriaDownload:
	def __init__(self, ariaControler, gid):
		assert isinstance(ariaControler, AriaControler)
		assert isinstance(gid, int)
		self.aria2 = ariaControler
		self.gid = gid    
	
	@property
	def status(self):
		self._updateStatus()
		return {"speed":self._speed,
				"connections": self._connections,
				"status": self._status,
				"completedLength": self._completedLength,
				"totalLength": self._toltalLength }
	
	def _updateStatus(self):
		rep = self.aria2.do_tellStatus(str(self.gid))
		self._speed = rep["downloadSpeed"]
		self._connections = rep["connections"]
		self._status = rep["status"]
		self._completedLength = rep["completedLength"]
		self._toltalLength = rep["totalLength"]

	def do_pause(self):
		rep = self.aria2.do_pause(self.gid)
		
	def do_unpause(self):
		rep = self.aria2.do_unpause(self.gid)
		
	def do_cancel(self):
		rep = self.aria2.do_remove(self.gid)
	
	def do_status(self):
		print "ok"	
	

class AriaControler:
	
	connection = None
	
	def __init__(self, server=None, port=None):
		self.connection = xmlrpclib.ServerProxy("http://localhost:6800/rpc")
	
	#Global action
	def do_addUri(self, uris):
		rep = self.connection.aria2.addUri([uris])
		return AriaDownload(self,int(rep))
	
	def do_pauseAll(self):
		""" Pause all downloads
		:returns:  bool -- the return code.
		"""
		rep = self.connection.aria2.pauseAll()
		if rep == "OK":
			return True
		else:
			print "DEBUG: "+str(rep)
			return False
		
	def do_unpauseAll(self):
		""" Unpause all downloads
		:returns:  bool -- the return code.
		"""
		rep = self.connection.aria2.unpauseAll()
		print rep
	
	def do_tellActive(self):
		rep = self.connection.aria2.tellActive()
		dls = []
		for download in rep:
			dls.append(AriaDownload(self,int(download["gid"])))
		return dls
	def do_tellWaiting(self,offset=0, num=10):
		self.connection.aria2.tellWaiting(offset, num)
	
	def do_tellStopped(self, offset=0, num=10):
		rep = self.connection.aria2.tellStopped(offset, num)
		dls = []
		for download in rep:
			dls.append(AriaDownload(self,int(download["gid"])))
		return dls
			
	def do_purgeDownloadResult(self):
		self.connection.aria2.purgeDownloadResult()

	
	# Download action
	def do_remove(self,gid):
		self.connection.aria2.remove(gid)
		
	def do_pause(self, gid):
		self.connection.aria2.pause(gid)
	
	def do_unpause(self, gid):
		self.connection.aria2.unpause(gid)
	
	def do_tellStatus(self, gid):
		return self.connection.aria2.tellStatus(gid)


if __name__ == '__main__':
	aria = AriaControler()
	app = REPL()
	app.register_formater(AriaDownload, AriaDownloadFormater)
	app.register_obj(aria)
	app.interactive()
