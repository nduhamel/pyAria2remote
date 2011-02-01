# -*- coding: utf-8 -*-
# Copyright(C) 2010  Nicolas Duhamel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
import cmd

from .lib.noconflict import classmaker
from .config import MetaConfig

from .utils import stdoutLock


class MetaCmd(type):
	pass

class Controler(cmd.Cmd, object):
	__metaclass__ = classmaker(right_metas=(MetaConfig,MetaCmd))
   
	def select(self, options, prompt='Your choice? '):
		'''Presents a numbered menu to the user.  Modelled after
		   the bash shell's SELECT.  Returns the item chosen.
		   
		   Argument ``options`` can be:

			 | a single string -> will be split into one-word options
			 | a list of strings -> will be offered as options
			 | a list of tuples -> interpreted as (value, text), so 
								   that the return value can differ from
								   the text advertised to the user '''
		if isinstance(options, basestring):
			options = zip(options.split(), options.split())
		fulloptions = []
		for opt in options:
			if isinstance(opt, basestring):
				fulloptions.append((opt, opt))
			else:
				try:
					fulloptions.append((opt[0], opt[1]))
				except IndexError:
					fulloptions.append((opt[0], opt[0]))
		self.poutput(prompt)
		for (idx, (value, text)) in enumerate(fulloptions):
			self.poutput('  %2d. %s\n' % (idx+1, text))
		while True:
			response = raw_input("Choice: ")
			try:
				response = int(response)
				result = fulloptions[response - 1][0]
				break
			except ValueError:
				pass # loop and ask again
		return result

	
	@stdoutLock()
	def poutput(self, msg):
		'''Convenient shortcut for self.stdout.write(); adds newline if necessary.'''
		if msg:
			self.stdout.write(msg)
			if msg[-1] != '\n':
				self.stdout.write('\n')
				
	def pfeedback(self, msg):
		if self.verbose:
			self.poutput(msg)
