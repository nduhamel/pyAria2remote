#!/usr/bin/python
import xmlrpclib
import logging, sys
import pprint

from repl import Formater, REPL
from utils import sizeof_fmt, simple_eta, achievepercent, ReadOnlyDict

logger = logging.getLogger()
hdlr = logging.FileHandler('/tmp/pyaria2remote.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


class AriaDownloadFormater(Formater):
	
	def __init__(self, ariadownload):
		assert isinstance(ariadownload, AriaDownload)
		self.download = ariadownload
	
	def pprint(self):		
		print "-------------------------------------------"
		with self.download:
			data = self.download.data
			print "id: "+data["gid"]+"  "+data["files"][0]["path"] + "   " + str(sizeof_fmt(int(data["completedLength"]))) + "/" + \
					 str(sizeof_fmt(int(data["totalLength"])))
			print "Speed: " + sizeof_fmt(int(data["downloadSpeed"])) + "/s     "  + \
				 str(achievepercent(int(data["totalLength"]), int(data["completedLength"]))) + "%"
		print "-------------------------------------------"

class AriaDownload(ReadOnlyDict):
	def __init__(self, ariaControler, gid):
		ReadOnlyDict.__init__(self)
		
		assert isinstance(ariaControler, AriaControler)
		assert isinstance(gid, int)
		self.aria2 = ariaControler
		self.gid = gid
	
	def __enter__(self):  self._updateStatus()
	def __exit__(self, exc_type, exc_value, traceback): pass
	
	def _updateStatus(self):
		rep = self.aria2.do_tellStatus(str(self.gid))
		self.update(rep)
	

class AriaControler:
		
	def __init__(self, server=None, port=None):
		self.connection = xmlrpclib.ServerProxy("http://localhost:6800/rpc")
		self.logger = logging.getLogger()
		

	def _do_cmd(self, cmd, *args):
		'''real xmlrpc command.'''
		server = self.connection
		try:
			fn = getattr(server, cmd)
			result = fn(*args)
			ppresult = pprint.pformat(result, 1)
			self.logger.debug("Call: "+ cmd )
			self.logger.debug("Response:\n "+ ppresult)
			return result
		except (xmlrpclib.Fault, xmlrpclib.ProtocolError):
			self.logger.error( '%s: %s' % (cmd, sys.exc_info()[1]) )


	##############
	### Repl cmd
	def do_addUri(self, uris):
		""" aria2.addUri return gid """
		rep = self._do_cmd("aria2.addUri", [uris])		
		return AriaDownload(self,int(rep))
	
	def do_pauseAll(self):
		"""Return OK on success """
		#~ rep = self.connection.aria2.pauseAll()
		rep = self._do_cmd("aria2.pauseAll")
		return rep
			
	def do_unpauseAll(self):
		"""Return OK on success """
		rep = self._do_cmd("aria2.unpauseAll")
		return rep
	
	def do_purgeDownloadResult(self):
		"""Return OK on success """
		rep = self._do_cmd("aria2.purgeDownloadResult")
		return rep

		
	def do_tellActive(self):
		""" aria2.tellActive return a list of download """
		rep = self._do_cmd("aria2.tellActive")
		dls = []
		for download in rep:
			dls.append(AriaDownload(self,int(download["gid"])))
		return dls
		
	def do_tellWaiting(self,offset=0, num=10):
		""" aria2.tellWaiting return a list of download """
		rep = self._do_cmd("aria2.tellWaiting", offset, num)
		dls = []
		for download in rep:
			dls.append(AriaDownload(self,int(download["gid"])))
		return dls
		
	def do_tellStopped(self, offset=0, num=10):
		""" aria2.tellStopped return a list of download """
		rep = self._do_cmd("aria2.tellStopped", offset, num)		
		dls = []
		for download in rep:
			dls.append(AriaDownload(self,int(download["gid"])))
		return dls

	def do_remove(self,gid):
		""" Return the removed download's gid """
		rep = self._do_cmd("aria2.remove", gid)
		return rep
		
	def do_pause(self, gid):
		""" Return the removed download's gid """
		rep = self._do_cmd("aria2.pause", gid)
		return rep
		
	def do_unpause(self, gid):
		""" Return the removed download's gid """
		rep = self._do_cmd("aria2.unpause", gid)
		return rep
			
	def do_tellStatus(self, gid):
		rep = self._do_cmd("aria2.tellStatus", gid)
		return rep


if __name__ == '__main__':
	aria = AriaControler()
	app = REPL()
	app.register_formater(AriaDownload, AriaDownloadFormater)
	app.register_obj(aria)
	app.interactive()
