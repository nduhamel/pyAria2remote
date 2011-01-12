#!/usr/bin/python
import xmlrpclib
import logging, sys

from repl import Formater, REPL
from utils import sizeof_fmt, simple_eta, achievepercent, ReadOnlyDict

from aria2 import AriaDownload, AriaControler

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


if __name__ == '__main__':
	aria = AriaControler()
	app = REPL()
	app.register_formater(AriaDownload, AriaDownloadFormater)
	app.register_obj(aria)
	app.interactive()
