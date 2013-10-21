# minimal sample showing how to write GTK3 indicator for Ubuntu Unity
# copyright 2012 Charl P. Botha <info@charlbotha.com>
# hereby released under the BSD license.
# https://bitbucket.org/cpbotha/indicator-cpuspeed/src

# use the PyGObject GObject introspection to use GTK+ 3 
# also see
# http://readthedocs.org/docs/python-gtk-3-tutorial/en/latest/index.html
# http://developer.gnome.org/gtk3/stable/ (API reference)

from gi.repository import Gtk, GLib

try: 
	from gi.repository import AppIndicator3 as AppIndicator  
except:  
	from gi.repository import AppIndicator

import re

class IndicatorCPUSpeed:
	def __init__(self):
		# param1: identifier of this indicator
		# param2: name of icon. this will be searched for in the standard them
		# dirs
		# finally, the category. We're monitoring CPUs, so HARDWARE.
		self.ind = AppIndicator.Indicator.new(
							"indicator-cpuspeed", 
							"",
							AppIndicator.IndicatorCategory.HARDWARE)

		# some more information about the AppIndicator:
		# http://developer.ubuntu.com/api/ubuntu-12.04/python/AppIndicator3-0.1.html
		# http://developer.ubuntu.com/resources/technologies/application-indicators/

		# need to set this for indicator to be shown
		self.ind.set_status (AppIndicator.IndicatorStatus.ACTIVE)

		# have to give indicator a menu
		self.menu = Gtk.Menu()

		# you can use this menu item for experimenting
		# item = Gtk.MenuItem()
		# item.set_label("Test")
		# item.connect("activate", self.handler_menu_test)
		# item.show()
		# self.menu.append(item)

		# this is for exiting the app
		item = Gtk.MenuItem()
		item.set_label("Exit")
		item.connect("activate", self.handler_menu_exit)
		item.show()
		self.menu.append(item)

		self.menu.show()
		self.ind.set_menu(self.menu)

		# initialize cpu speed display
		self.update_cpu_speeds()
		# then start updating every 2 seconds
		# http://developer.gnome.org/pygobject/stable/glib-functions.html#function-glib--timeout-add-seconds
		GLib.timeout_add_seconds(2, self.handler_timeout)

	def get_cpu_speeds(self):
		"""Use regular expression to parse speeds of all CPU cores from
		/proc/cpuinfo on Linux.
		"""

		f = open('/proc/cpuinfo')
		# this gives us e.g. ['2300', '2300']
		s = re.findall('cpu MHz\s*:\s*(\d+)\.', f.read())
		# this will give us ['2.3', '2.3']
		f = ['%.1f' % (float(i) / 1000,) for i in s]
		return f

	def handler_menu_exit(self, evt):
		Gtk.main_quit()

	def handler_menu_test(self, evt):
		# we can change the icon at any time
		self.ind.set_icon("indicator-messages-new")

	def handler_timeout(self):
		"""This will be called every few seconds by the GLib.timeout.
		"""
		# read, parse and put cpu speeds in the label
		self.update_cpu_speeds()
		# return True so that we get called again
		# returning False will make the timeout stop
		return True

	def update_cpu_speeds(self):
		f = self.get_cpu_speeds()
		self.ind.set_label('00:15:00', "..XX:XX:XX..")

	def main(self):
		Gtk.main()

if __name__ == "__main__":
	ind = IndicatorCPUSpeed()
	ind.main()

