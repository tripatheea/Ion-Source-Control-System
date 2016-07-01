import gi

gi.require_version('Gtk', '3.0')

import copy
import time
import random
import threading
import datetime
import uuid


import control_system_serial
import serial

from gi.repository import Gtk, GLib, GObject, Gdk

from procedure import Procedure
from serial import SerialException
from device import Device, Channel
from MIST1_Control_System_GUI_Widgets import *

import data_logging

import dialogs as MIST1Dialogs
from MPLCanvasWrapper3 import MPLCanvasWrapper3



import numpy as np
from matplotlib.figure import Figure
import matplotlib.cm as cm



from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar


# Maybe have a dedicated add_channel() method just like add_device() so that it can take care of everything, like adding the correct channel to the logger, updating the tree view, etc.

__author__ = "Aashish Tripathee and Daniel Winklehner"
__doc__ = """GUI without actual functionality"""

class MIST1ControlSystem:
	"""
	Main class that runs the GUI for the MIST-1 control system
	"""

	def __init__(self):
		"""
		Initialize the control system GUI
		"""
		# --- Load the GUI from XML file and initialize connections --- #
		self._builder = Gtk.Builder()
		self._builder.add_from_file("mist_control_system_main_gui.glade")
		self._builder.connect_signals(self.get_connections())

		self._main_window = self._builder.get_object("main_window")
		self._arduino_vbox = self._builder.get_object("arduino_vbox")

		# --- Get some widgets from the builder --- #
		self._status_bar = self._builder.get_object("main_statusbar")
		self._log_textbuffer = self._builder.get_object("log_texbuffer")
		self._overview_grid = self._builder.get_object("overview_grid")

		self._emergency_stop_button = self._builder.get_object("stop_button")
		self._emergency_stop_button.set_name("stop_button")

		# --- Paint the stop button red! --- #
		style_provider = Gtk.CssProvider()

		css = """
		GtkButton#stop_button {
			color: #000000;
			font-size: 18pt;
			background-image: url('bg.png');
		}
		"""

		style_provider.load_from_data(css)

		Gtk.StyleContext.add_provider_for_screen(
			Gdk.Screen.get_default(),
			style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
		)

		# --- The main device dict --- #
		self._devices = {}

		# --- The serialCOM dict --- #
		self._serial_comms = {}

		self._initialized = False

		self._keep_communicating = False
		self._communication_threads = {}

		# key = device_name, value = 'read' / 'write' i.e. which direction the communication is
		# supposed to happen. It's from POV of the GUI i.e. the direction is GUI -> Arduino.
		self._communication_threads_mode = {}
		self._communication_threads_poll_count = {}
		self._communication_threads_start_time = {}
		self._arduino_status_bars = {}

		self._set_value_for_widget = None	

		# HDF5 logging.
		self._data_logger = None

		self._last_checked_for_devices_alive = time.time()
		self._alive_device_names = set()
		self._check_for_alive_interval = 5	# In seconds.


		self._edit_frame = None
		
		# self._settings_tree_view = None
		# self._settings_page_tree_store = None

		self._settings_page_tree_store = Gtk.TreeStore(str, str, str, str, str)
		self._settings_tree_view = Gtk.TreeView(self._settings_page_tree_store)

		# self.setup_settings_page()


		self._keep_procedure_thread_running = False
		self._procedures = {}
		self._procedure_thread = None


		self._keep_critical_procedure_threads_running = False
		self._critical_procedures = {}	 # These get their own threads.
		self._critical_procedure_threads = {}

		self._plot_page_channels_tree_store = Gtk.TreeStore(Gtk.CheckButton, str, str, str, str)
		self._plot_page_channels_tree_view = Gtk.TreeView(self._plot_page_channels_tree_store)

		self._plotting_page_grid = None
		self._plotting_frames = {}	# Dictionary of all plotting frames. Keys = Tuples(device_name, channel_name).


		


	def register_data_logging_file(self, filename):
		self._data_logger = data_logging.DataLogging(log_filename=filename)
		self._data_logger.initialize()

	
	def log_data(self, channel):
		self._data_logger.log_value(channel=channel)
		# pass
	

	def about_program_callback(self, menu_item):
		"""
		:param menu_item:
		:return:
		"""
		dialog = self._builder.get_object("about_dialogbox")
		dialog.run()
		dialog.destroy()

		return 0


	def add_device_callback(self, button):
		dialog = MIST1Dialogs.AddDevicesDialog(self._main_window)
		
		dialog.add_pre_existing_devices(self._devices)

		dialog.initialize()

		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			# Reinitialize all devices.
			for device_name, device in self._devices.items():
				if not device.initialized():
					del self._devices[device_name]
					print "Adding a new device."
					self.add_device(device)

			self.reinitialize()

		elif response == Gtk.ResponseType.CANCEL:
			print("The Cancel button was clicked")

		dialog.destroy()




	def edit_device_callback(self, button):
		
		dialog = MIST1Dialogs.EditDevicesDialog(self._main_window)
		
		dialog.add_pre_existing_devices(self._devices)

		dialog.initialize()

		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			# Reinitialize all devices.
			
			print "Save Changes clicked."

			# for device_name, device in self._devices.items():
				
			# 	# if not device.initialized():
			# 	# 	del self._devices[device_name]
			# 	# 	print "Adding a new device."
			# 	# 	self.add_device(device)

			self.reinitialize()

		elif response == Gtk.ResponseType.CANCEL:
			print("The Cancel button was clicked")

		dialog.destroy()



		


	def load_device_from_file_callback(self, button):

		dialog = Gtk.FileChooserDialog("Please choose a file.", self._main_window,
										Gtk.FileChooserAction.OPEN,
										(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
										Gtk.STOCK_OPEN, Gtk.ResponseType.OK),
										)

		filter_text = Gtk.FileFilter()
		filter_text.set_name("JSON files")
		filter_text.add_mime_type("application/json")
		dialog.add_filter(filter_text)

		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			filename = dialog.get_filename()

			print("Open clicked")
			print("File selected: " + filename)

			device = Device.load_from_json(filename)

			if device.name() not in self._devices.keys():
				self.add_device(device)

				self.initialize()

				self._devices[device.name()].get_overview_frame().show_all()


		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")

		dialog.destroy()

		return 0


	def set_widget_connections(self):
		for device_name, device in self._devices.items():
			for channel_name, channel in device.channels().items():

				if channel.mode() == "both" or channel.mode() == "write":	# TODO: Find a better way to do this.

					widget = channel.get_overview_page_display()
					
					try:	# According to http://stackoverflow.com/questions/1549801/differences-between-isinstance-and-type-in-python, better to use try-except than check type / instanceof.
						widget.get_radio_buttons()[0].connect("toggled", self.set_value_callback, widget)
					except Exception as e:
						pass



	def add_arduino_status_bar(self, arduino_id, status_bar):
		self._arduino_status_bars[arduino_id] = status_bar


	def add_channel(self, channel, device):

		if channel.name() not in device.channels().keys():

			# Add channel to device.
			device.add_channel( channel )

			channel.initialize()

			# Add channel to logger.
			self._data_logger.add_channel(channel)

			self._main_window.show_all()

			# Add channel to settings page tree. 
			# First, find the position of device in the iterator. 

			for i in range(len(self._settings_page_tree_store)):
				if device.name() == self._settings_page_tree_store[i][-1]:
					position = i
					device_path = Gtk.TreePath.new_from_string( "{}".format(i) )
					device_iter = self._settings_page_tree_store.get_iter(device_path)
					break

			print device_iter, self._settings_page_tree_store.get_value(device_iter, 0)

			channel_iter = self._settings_page_tree_store.insert( device_iter, 0, [channel.label(), "Channel", "edit_channel", channel.name(), device.name()] )

			print channel_iter, self._settings_page_tree_store.get_value(channel_iter, 0)

			channel_iter = self._settings_page_tree_store.append(device_iter, ["<b>[ Add a New Channel ]</b>", "", "add_new_channel", device.name(), device.name()])


			self._settings_tree_view.show_all()

		return 0

	def add_procedure(self, procedure):
		# TODO: NOT IN USE RIGHT NOW.

		if procedure.get_priority() == -1:
			# Gets its own thread so is a "critical" procedure.
			self._critical_procedures[procedure.get_name()] = procedure
		else:
			self._procedures[procedure.get_name()] = procedure



	def add_device(self, device):
		"""
		Adds a device to the control system
		:return:
		"""
		# Set the control system as the device parent
		device.set_parent(self)

		# Add device to the list of devices in the control system
		self._devices[device.name()] = device


		# Add corresponding channels to the hdf5 log.
		for channel_name, channel in device.channels().items():
			if channel.mode() == "read" or channel.mode() == "both":
				self._data_logger.add_channel(channel)

		# Add the device to the settings page tree.

		device_iter = self._settings_page_tree_store.insert( None, (len(self._settings_page_tree_store) - 1), [device.label(), "Device", "edit_device", device.name(), device.name()] )
		
		for channel_name, channel in device.channels().items():
			channel_iter = self._settings_page_tree_store.append(device_iter, [channel.label(), "Channel", "edit_channel", channel.name(), device.name()])

		channel_iter = self._settings_page_tree_store.append(device_iter, ["<b>[ Add a New Channel ]</b>", "", "add_new_channel", device.name(), device.name()])


		self._settings_tree_view.show_all()

		return 0

	def add_serial_com(self, serial_com):
		self._serial_comms[serial_com.arduino_id()] = serial_com


	def set_value_callback(self, button, widget):
		
		# print "Set callback called by {}".format(widget.get_name())

		parent_channel = widget.get_parent_channel()

		self._set_value_for_widget = widget
		self._communication_threads_mode[parent_channel.get_arduino_id()] = "write"

	def listen_for_reconnected_devices(self, devices):
		for device in devices:
			if device.name() in self._devices.keys() and device.name() not in self._alive_device_names:
				print "Reinitializing device ", device.name()
				device.reinitialize()


	def check_for_alive_devices(self, devices):
		# Check which Arduinos are still alive.

		for device in devices:
			if device.get_serial_com().is_alive():
				
				self._alive_device_names.add(device.name())

				if device.locked():
					device.unlock()
			else:
				print "Device = {} not alive.".format(device.name())
				print "Locking device", device.name()
				device.lock()
				self._alive_device_names.discard(device.name())

		self._last_checked_for_devices_alive =  time.time()

		print "The set of all alive devices = ", self._alive_device_names

	def communicate(self, devices):
		"""
		:param devices:
		:return:
		"""

		while self._keep_communicating:
			
			# if (time.time() - self._last_checked_for_devices_alive) > self._check_for_alive_interval:
			# 	self.check_for_alive_devices(devices)
			# 	self.listen_for_reconnected_devices(devices)

			# GLib.idle_add(self.dummy_update)

			for device in devices:

				# For each device that belonds to the same arduino (i.e same thread) we do this
				# Find out whether we're supposed to read in values or write values at this time.

				# THOUGHT: Maybe implement a device.locked thing and don't operate on a given device unless that lock is released?
				# Ideally, even all the methods in the Device class would respect that lock. 
				
				if not device.locked():


					arduino_id = device.get_arduino_id()

					# print "Trying to communicate with device {} @ arduino {}".format(device.name(), arduino_id)

					if self._communication_threads_mode[arduino_id] == "read":

						# Find all the channels, see if they are in 'read' or 'both' mode,
						# then update the widgets with those values.

						for channel_name, channel in device.channels().items():

							# if channel.initialized() and (channel.mode() == "read" or channel.mode() == "both"):
							if (channel.mode() == "read" or channel.mode() == "both"):

								try:
									channel.read_value()

									try:
										# Log data.
										self.log_data(channel)
									except Exception as e:
										# print "Exception caught while trying to log data."
										# print e
										pass

									self._communication_threads_poll_count[arduino_id] += 1

									GLib.idle_add(self.update_gui, channel)

								except Exception as e:
									"Got an exception", e

					elif self._communication_threads_mode[arduino_id] == "write" and self._set_value_for_widget is not None:
						
						print "Setting value."

						widget_to_set_value_for = self._set_value_for_widget
						channel_to_set_value_for = self._set_value_for_widget.get_parent_channel()

						print "Communicating updated value for widget {}".format( widget_to_set_value_for.get_name() )

						# Check if the channel is actually a writable channel (channel.mode() ?= "write" or "both").
						
						if channel_to_set_value_for.mode() == "write" or channel_to_set_value_for.mode() == "both":
		
							try:
								value_to_update = widget_to_set_value_for.get_value()
							except ValueError:
								value_to_update = -1

							
							print "Setting value = {}".format(value_to_update)

							try:
								channel_to_set_value_for.set_value(value_to_update)
							except Exception, e:
								# Setting value failed. There was some exception.
								# Write the error message to the status bar.
								self._status_bar.push(2, str(e))


						self._communication_threads_mode[arduino_id] = "read"
						self._set_value_for_widget = None

		print "Closing communication thread."

		return 0

	def emergency_stop(self, widget):
		"""
		Callback for STOP button, but may also be called if interlock is broken or
		in any other unforseen sircumstance that warrants shutting down all power supplies.
		:param widget:
		:return:
		"""

		self._status_bar.push(1, "Emergency stop button was pushed!")
		self.shut_down_communication_threads()

		return 0


	def monitor_procedures(self):
		# TODO: NOT IN USE RIGHT NOW.

		# This is the method that all non-critical procedure threads run.

		while self._keep_procedure_thread_running:

			# print "Monitoring all non-critical threads here."

			# TODO:
			# THOUGHT: Should this also have a while loop? I mean, so that we keep on trying to do the procedure until it succeeds.

			for procedure_name, procedure in self._procedures.items():
				if procedure.should_perform_procedure():
					procedure.act()
			

	def monitor_critical_procedure(self, critical_procedure):

		# TODO: NOT IN USE RIGHT NOW.

		# This is the method that all critical procedure threads run. Each of them run in a separate thread.


		while self._keep_critical_procedure_threads_running:


			# print "Critical thread running on its own thread."
			

			# Technically, we don't have to check this here since it's checked in the Procedure class before actually performing the procedure.
			# But double-checking it probably won't hurt (will have some non-zero cost associated with retrieving values and then computing whether or not all the conditions are satisfied).
			

			# The second conditional is so that we can keep trying to perform the procedure until we succeed. This is crucial for "critical" procedures.
			while critical_procedure.should_perform_procedure() and (not critical_procedure.act()):	
				critical_procedure.act()

			


	def setup_procedure_threads(self):
		# TODO: NOT IN USE RIGHT NOW.
		
		# For N critical threads, there's going to be (N + 1) total threads. The N threads are one each for the "crtical" (procedure.priority = -1) procedures. All remaining procedures are processed with just 1 thread.

		# TODO: Need to implement proper thread waiting, especially for "critical" threads. 
		# Because critical threads need to have higher priorities than "communication threads". 

		# First, setup a general thread i.e. one thread for all non-critical procedures.


		# TODO: THOUGHT: We could pass a list / dictionary of all the procedures we want to monitor here as kwargs.
		# But, that way, the thread would only act only on those procedures that were created at the very beginning. 
		# There wouldn't be a straightforward way for this thread to also handle the procedures that were added later on.

		if self._procedure_thread == None:
			self._procedure_thread = threading.Thread(target=self.monitor_procedures)
			
			self._keep_procedure_thread_running = True

			self._procedure_thread.start()

		# Next, setup one thread each for each of the critical procedures we have.
		for critical_procedure_name, critical_procedure in self._critical_procedures.items():
			
			critical_procedure_thread = threading.Thread(target=self.monitor_critical_procedure)

			self._critical_procedure_threads[critical_procedure_name] = critical_procedure_thread

			self._keep_critical_procedure_threads_running = True

			self._critical_procedure_threads[critical_procedure_name].start()

		pass

	def setup_communication_threads(self):
		"""
		For each device, we create a thread to communicate with the corresponding Arduino.
		:return:
		"""
		for arduino_id, serial_com in self._serial_comms.items():

			if arduino_id not in self._communication_threads.keys():

				my_devices = [dev for devname, dev in self._devices.items() if arduino_id == dev.get_arduino_id()]

				communication_thread = threading.Thread(target=self.communicate,
														kwargs=dict(devices=my_devices))

				self._communication_threads[arduino_id] = communication_thread
				self._communication_threads_mode[arduino_id] = 'read'
				self._communication_threads_poll_count[arduino_id] = 0
				self._communication_threads_start_time[arduino_id] = time.time()

				self._keep_communicating = True

				self._communication_threads[arduino_id].start()

		return 0

	def get_arduino_vbox(self):
		return self._arduino_vbox


	def save_as_devices_callback(self, button):
		
		def select_all_callback(widget, checkboxes):
			for device_name, checkbox in checkboxes.items():
				checkbox.set_active(True)

		def unselect_all_callback(widget, checkboxes):
			for device_name, checkbox in checkboxes.items():
				checkbox.set_active(False)


		dialog = Gtk.FileChooserDialog("Save Device", self._main_window,
										Gtk.FileChooserAction.SELECT_FOLDER,
										(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
										("_Save"), Gtk.ResponseType.OK),
										)


		content_area = dialog.get_content_area()
	

		select_all_label = Gtk.Button("Select All")
		unselect_all_label = Gtk.Button("Unselect All")

		device_checkboxes = {}
		for device_name, device in self._devices.items():
			device_checkboxes[device.name()] = Gtk.CheckButton(device.label())


		info_frame = Gtk.Frame(label="Select Devices To Save", margin=4)
		info_frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
		info_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4, margin=4)
		info_frame.add( info_vbox )


		select_all_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1, margin=4)
		
		

		select_all_hbox.pack_start(select_all_label, expand=False, fill=False, padding=5) 
		select_all_hbox.pack_start(unselect_all_label, expand=False, fill=False, padding=5) 
	
		select_all_handler_id = select_all_label.connect("clicked", select_all_callback, device_checkboxes)
		select_all_handler_id = unselect_all_label.connect("clicked", unselect_all_callback, device_checkboxes)

		device_name_hboxes = []

		for device_name, checkbox in device_checkboxes.items():
			hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1, margin=4)

			hbox.pack_start(checkbox, expand=True, fill=True, padding=0) 

			device_name_hboxes.append( hbox )


		info_vbox.pack_start(select_all_hbox, expand=True, fill=True, padding=0) 

		for hbox in device_name_hboxes:
			info_vbox.pack_start(hbox, expand=True, fill=True, padding=0) 
		

		
		

		content_area.add( info_frame )

		content_area.pack_start(info_vbox, expand=False, fill=False, padding=0)


		info_vbox.reorder_child(info_vbox, 0)
		
		dialog.show_all()

		response = dialog.run()


		if response == Gtk.ResponseType.OK:
			directory = dialog.get_filename()

			device_count = 0
			for device_name, device in self._devices.items():
				
				if device_checkboxes[device_name].get_active():
					device.write_json(directory + "/" + device_name + ".json")
					device_count += 1

			msg_dialog = Gtk.MessageDialog(dialog, 0, Gtk.MessageType.INFO,
			Gtk.ButtonsType.OK, "Device Save Successful")

			noun = "device"
			if device_count > 1:
				noun += "s"

			msg_dialog.format_secondary_text( "Successfully saved {} {} to {}.".format(device_count, noun, directory) )
			msg_dialog.run()

			msg_dialog.destroy()


		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")

		dialog.destroy()

	
	def settings_expand_all_callback(self, button):
		self._settings_tree_view.expand_all()

	def settings_collapse_all_callback(self, button):
		self._settings_tree_view.collapse_all()


	def get_connections(self):
		"""
		This just returns a dictionary of connections
		:return:
		"""
		con = {"main_quit": self.main_quit,
			   "stop_button_clicked_cb": self.emergency_stop,
			   "on_main_statusbar_text_pushed": self.statusbar_changed_callback,
			   "about_program_menu_item_activated": self.about_program_callback,
			   "add_device_toolbutton_clicked_cb": self.add_device_callback,
			   "edit_device_toolbutton_clicked_cb": self.edit_device_callback,
			   "load_device_from_file_toolbutton_cb": self.load_device_from_file_callback,
			   "save_as_devices_toolbutton_clicked_cb": self.save_as_devices_callback,
			   "settings_expand_all_clicked_cb": self.settings_expand_all_callback,
			   "settings_collapse_all_clicked_cb": self.settings_collapse_all_callback,

			   }

		return con

	def get_overview_grid(self):
		return self._overview_grid

	def get_serial_comms(self):
		return self._serial_comms

	def initialize(self):
		"""
		:return:
		"""
		# Initialize the ankered devices first
		for device_name, device in self._devices.items():

			device.initialize()

		# Setup connections for widgets (for radio buttons for example).
		self.set_widget_connections()

		# Any and all remaining initializations go here
		self.setup_communication_threads()

		self.setup_settings_page()

		self.setup_plotting_page()


		# self.setup_procedure_threads() 




		self._initialized = True

		return 0

	def settings_add_device_callback(self, button, params):

		device_name = params['name'].get_text()
		device_label = params['label'].get_text()
		arduino_id = params['arduino_id'].get_text()
		overview_page_presence = params['overview_page_presence'].get_active()

		print "Got a new device!"

		new_device = Device(name=device_name, label=device_label, arduino_id=arduino_id)
		new_device.set_overview_page_presence(overview_page_presence)

		self.add_device(new_device)

		self.reinitialize()

		# if self._edit_frame != None:
		# 	self._builder.get_object("settings_page_settings_box").remove(self._edit_frame)


	def settings_add_channel_callback(self, button, device_name, params):
		# Default values.
		data_type, mode = float, "both"

		data_type_iter = params['data_type'].get_active_iter()

		if data_type_iter != None:
			model = params['data_type'].get_model()
			data_type, data_type_str = model[data_type_iter][:2]
			data_type = eval(data_type)


		mode_iter = params['mode'].get_active_iter()

		if mode_iter != None:
			model = params['mode'].get_model()
			mode, mode_str = model[mode_iter][:2]


		# Create a new channel.
		ch = Channel(name=params['name'].get_text(), 
					 label=params['label'].get_text(),
					 message_header=params['message_header'].get_text(),
					 upper_limit=float(params['upper_limit'].get_text()),
					 lower_limit=float(params['lower_limit'].get_text()),
					 data_type=data_type,
					 mode=mode,
					 unit=params['unit'].get_text())


		# Add the newly created channel to the correct device.


		self.add_channel(ch, self._devices[device_name])

		# if self._edit_frame != None:
		# 	self._builder.get_object("settings_page_settings_box").remove(self._edit_frame)

		

	def device_settings_tree_selection_callback(self, selection):
		
		if self._edit_frame != None:
			self._builder.get_object("settings_page_settings_box").remove(self._edit_frame)


		model, treeiter = selection.get_selected()
		
		if treeiter != None:

			label = model[treeiter][0]
			object_type = model[treeiter][1]
			selection_type = model[treeiter][2]
			name = model[treeiter][3]
			device_name = model[treeiter][4]
			

			
			edit_device_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin=12)

			if selection_type == "edit_device":

				# Populate the right-side-box with fields to edit device information.
				device = self._devices[device_name]

				self._edit_frame = Gtk.Frame(label="Edit {}".format(label))
				self._edit_frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
				self._edit_frame.add( edit_device_vbox )

				grid = Gtk.Grid(column_spacing=20, row_spacing=15)
				edit_device_vbox.add(grid)

				labels = ["Name", "Label", "Arduino ID", "Overview Page Presence"]
				entries = [Gtk.Entry(), Gtk.Entry(), Gtk.Entry(), Gtk.CheckButton()]
				values = [device.name(), device.label(), device.get_arduino_id(), device.is_on_overview_page()]

				for label_text, entry, value in zip(labels, entries, values):

					label = Gtk.Label(xalign=1)
					label.set_markup("<span foreground='#888a85'>" + label_text + "</span>")

					if label_text == "Name":
						grid.add(label)
						grid.attach_next_to(entry, label, Gtk.PositionType.RIGHT, width=20, height=1)
					else:
						grid.attach_next_to(label, last_label, Gtk.PositionType.BOTTOM, width=1, height=1)
						grid.attach_next_to(entry, last_entry, Gtk.PositionType.BOTTOM, width=20, height=1)
					
					entry_type = str(type(entry)).split("'")[1]

					if entry_type == "gi.repository.Gtk.Entry":
						entry.set_text(value)
					elif entry_type == "gi.repository.Gtk.CheckButton":
						entry.set_active(value)

					last_entry, last_label = entry, label

				edit_device_save_button = Gtk.Button(label="Save Changes to Device")
				grid.attach_next_to(edit_device_save_button, last_entry, Gtk.PositionType.BOTTOM, width=20, height=1)

			elif selection_type == "add_new_device":

				self._edit_frame = Gtk.Frame(label="Add a New Device")
				self._edit_frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
				self._edit_frame.add( edit_device_vbox )

				grid = Gtk.Grid(column_spacing=20, row_spacing=15)
				edit_device_vbox.add(grid)

				labels = ["Name", "Label", "Arduino ID", "Overview Page Presence"]
				entries = [Gtk.Entry(), Gtk.Entry(), Gtk.Entry(), Gtk.CheckButton()]

				
				for label_text, entry in zip(labels, entries):
					
					label = Gtk.Label(xalign=1)
					label.set_markup("<span foreground='#888a85'>" + label_text + "</span>");

					if label_text == "Name":
						grid.add(label)
						grid.attach_next_to(entry, label, Gtk.PositionType.RIGHT, width=20, height=1)
					else:
						grid.attach_next_to(label, last_label, Gtk.PositionType.BOTTOM, width=1, height=1)
						grid.attach_next_to(entry, last_entry, Gtk.PositionType.BOTTOM, width=20, height=1)

					last_entry, last_label = entry, label

				add_device_button = Gtk.Button(label="Add Device")	
				add_device_button.connect("clicked", self.settings_add_device_callback, dict(name=entries[0], label=entries[1], arduino_id=entries[2], overview_page_presence=entries[3]))
				grid.attach_next_to(add_device_button, last_entry, Gtk.PositionType.BOTTOM, width=20, height=1)
				

			elif selection_type == "edit_channel":

				device = self._devices[device_name]
				channel = device.channels()[name]

				self._edit_frame = Gtk.Frame(label="Edit {}".format(label))
				self._edit_frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
				self._edit_frame.add( edit_device_vbox )

				grid = Gtk.Grid(column_spacing=20, row_spacing=15)
				edit_device_vbox.add(grid)

				labels = ["Name", "Label", "Message Header", "Lower Limit", "Upper Limit", "Unit"]
				entries = [Gtk.Entry(), Gtk.Entry(), Gtk.Entry(), Gtk.Entry(), Gtk.Entry(), Gtk.Entry()]
				values = [channel.name(), channel.label(), channel.message_header(), channel.lower_limit(), channel.upper_limit(), channel.unit() ]

				for label_text, entry, value in zip(labels, entries, values):

					label = Gtk.Label(xalign=1)
					label.set_markup("<span foreground='#888a85'>" + label_text + "</span>")

					if label_text == "Name":
						grid.add(label)
						grid.attach_next_to(entry, label, Gtk.PositionType.RIGHT, width=20, height=1)
					else:
						grid.attach_next_to(label, last_label, Gtk.PositionType.BOTTOM, width=1, height=1)
						grid.attach_next_to(entry, last_entry, Gtk.PositionType.BOTTOM, width=20, height=1)

					entry.set_text(str(value))

					last_entry, last_label = entry, label



				data_type_model_view = Gtk.ListStore(str, str)
				data_type_options = [ ["bool", "Boolean"], ["int", "Integer"], ["float", "Float"] ]

				for option in data_type_options:
					data_type_model_view.append( option )
				
				data_type_combo = Gtk.ComboBox.new_with_model_and_entry(data_type_model_view)
				data_type_combo.set_entry_text_column(1)
				data_type_combo.set_active( [x for x, y in data_type_options].index( str(channel.data_type()).split("'")[1] ) )
				
				label = Gtk.Label(xalign=1)
				label.set_markup("<span foreground='#888a85'>Data Type</span>")

				grid.attach_next_to(label, last_label, Gtk.PositionType.BOTTOM, width=1, height=1)
				grid.attach_next_to(data_type_combo, last_entry, Gtk.PositionType.BOTTOM, width=20, height=1)

				last_entry = data_type_combo
				last_label = label
				

				mode_model_view = Gtk.ListStore(str, str)
				mode_options = [ ["read", "Read"], ["write", "Write"], ["both", "Both"] ]

				for option in mode_options:
					mode_model_view.append( option )
				
				mode_combo = Gtk.ComboBox.new_with_model_and_entry(mode_model_view)
				mode_combo.set_entry_text_column(1)
				mode_combo.set_active( [x for x, y in mode_options].index( channel.mode() ) )
				
				label = Gtk.Label(xalign=1)
				label.set_markup("<span foreground='#888a85'>Mode</span>")

				grid.attach_next_to(label, last_label, Gtk.PositionType.BOTTOM, width=1, height=1)
				grid.attach_next_to(mode_combo, last_entry, Gtk.PositionType.BOTTOM, width=20, height=1)

				last_entry, last_label = mode_combo, label
				
				edit_channel_save_button = Gtk.Button(label="Save Changes to Channel")
				grid.attach_next_to(edit_channel_save_button, last_entry, Gtk.PositionType.BOTTOM, width=20, height=1)

			elif selection_type == "add_new_channel":
				device = self._devices[device_name]
				

				self._edit_frame = Gtk.Frame(label="Add a New Channel to {}".format(device.label()))
				self._edit_frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
				self._edit_frame.add( edit_device_vbox )

				grid = Gtk.Grid(column_spacing=20, row_spacing=15)
				edit_device_vbox.add(grid)



				labels = ["Name", "Label", "Message Header", "Lower Limit", "Upper Limit", "Unit"]
				entries = [Gtk.Entry(), Gtk.Entry(), Gtk.Entry(), Gtk.Entry(), Gtk.Entry(), Gtk.Entry()]

				for label_text, entry in zip(labels, entries):
					
					label = Gtk.Label(xalign=1)
					label.set_markup("<span foreground='#888a85'>" + label_text + "</span>")

					if label_text == "Name":
						grid.add(label)
						grid.attach_next_to(entry, label, Gtk.PositionType.RIGHT, width=20, height=1)
					else:
						grid.attach_next_to(label, last_label, Gtk.PositionType.BOTTOM, width=1, height=1)
						grid.attach_next_to(entry, last_entry, Gtk.PositionType.BOTTOM, width=20, height=1)

					last_entry = entry
					last_label = label


				data_type_model_view = Gtk.ListStore(str, str)
				data_type_options = [ ["bool", "Boolean"], ["int", "Integer"], ["float", "Float"] ]

				for option in data_type_options:
					data_type_model_view.append( option )
				
				data_type_combo = Gtk.ComboBox.new_with_model_and_entry(data_type_model_view)
				data_type_combo.set_entry_text_column(1)
				data_type_combo.set_active( [x for x, y in data_type_options].index( "float" ) )
				
				label = Gtk.Label(xalign=1)
				label.set_markup("<span foreground='#888a85'>Data Type</span>")

				grid.attach_next_to(label, last_label, Gtk.PositionType.BOTTOM, width=1, height=1)
				grid.attach_next_to(data_type_combo, last_entry, Gtk.PositionType.BOTTOM, width=20, height=1)

				last_entry = data_type_combo
				last_label = label
				

				mode_model_view = Gtk.ListStore(str, str)
				mode_options = [ ["read", "Read"], ["write", "Write"], ["both", "Both"] ]

				for option in mode_options:
					mode_model_view.append( option )
				
				mode_combo = Gtk.ComboBox.new_with_model_and_entry(mode_model_view)
				mode_combo.set_entry_text_column(1)
				mode_combo.set_active( [x for x, y in mode_options].index( "read" ) )
				
				label = Gtk.Label(xalign=1)
				label.set_markup("<span foreground='#888a85'>Mode</span>")

				grid.attach_next_to(label, last_label, Gtk.PositionType.BOTTOM, width=1, height=1)
				grid.attach_next_to(mode_combo, last_entry, Gtk.PositionType.BOTTOM, width=20, height=1)

				last_entry, last_label = mode_combo, label


				add_device_button = Gtk.Button(label="Add Channel")
				add_device_button.connect("clicked", self.settings_add_channel_callback, device_name, dict( name=entries[0], label=entries[1], message_header=entries[2], lower_limit=entries[3], upper_limit=entries[4], unit=entries[5], data_type=data_type_combo, mode=mode_combo ) )
				grid.attach_next_to(add_device_button, last_entry, Gtk.PositionType.BOTTOM, width=20, height=1)

			self._builder.get_object("settings_page_settings_box").add(self._edit_frame)




		self._main_window.show_all()




	def test_function(self, axis):

		X = np.arange(100)
		Y = X * X

		axis.plot(X, Y, c = "blue", label = "test0", linestyle = "solid")
		self.canvas.append_legend_entries_flag(True)

		axis.plot(X, X, c = "green", label = "test1", linestyle = "solid")
		self.canvas.append_legend_entries_flag(True)

		axis.scatter(X, Y*1.2, s = 5**2, c = "red", edgecolor = "red", label = "test2", marker = "o")
		self.canvas.append_legend_entries_flag(True)

		return 0


	def remove_plotting_frame(self, device_name, channel_name):
		plotting_frame = self._plotting_frames[(device_name, channel_name)]

		self._plotting_page_grid.remove(plotting_frame)

		del self._plotting_frames[(device_name, channel_name)]

	def show_plotting_frame(self, device_name, channel_name):
			
		print "Showing plotting frame for", device_name, channel_name

		device = self._devices[device_name]
		channel = device.channels()[channel_name]

		# Create a new frame.

		plot_frame = Gtk.Frame(label="{} : {}".format(device.label(), channel.label()))
		plot_frame.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
		self._plotting_frames[(device_name, channel_name)] = plot_frame

		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		box.set_size_request(200, 200)


		plot_frame.add(box)

		self.canvas = MPLCanvasWrapper3(nbp=0)
		box.pack_start(self.canvas, True, True, 0)

		self.test_function(self.canvas.axis)
		self.canvas.set_autoscale(True)
		

		self._plotting_page_grid.add(plot_frame)

		self._plotting_page_grid.show_all()


	def plotting_page_on_channel_toggle(self, cell, path, store, *ignore):
		if path is not None:
			it = store.get_iter(path)

			print "The current state is", store[it][0].get_active()

			store[it][0].set_active( not store[it][0].get_active() )

			print "After changing it, the updated state is", store[it][0].get_active()

			# Find out which channel it was.
			device_name = store.get_value( store.get_iter(path), 3 )

			if device_name == store.get_value( store.get_iter(path), 4 ):
				# This means the users selected a checkbox for a device. 
				# Activate all channels under this device.
				pass

			else:
				channel_name = store.get_value( store.get_iter(path), 4 )
				
				if store[it][0].get_active():
					self.show_plotting_frame(device_name, channel_name)
				else:
					self.remove_plotting_frame(device_name, channel_name)

		self._plot_page_channels_tree_view.show_all()
			

	def setup_plotting_page(self):


		self._plotting_page_grid = Gtk.Grid(column_spacing=30, row_spacing=150, margin=100)
		self._plotting_page_grid.set_column_homogeneous(True)
		self._plotting_page_grid.set_row_homogeneous(True)

		plotting_page_plots_box = self._builder.get_object("plotting_page_plots_box")
		plotting_page_plots_box.add(self._plotting_page_grid)




		plotting_scrolled_window = self._builder.get_object("plotting_scrolled_window")
		
		# _plot_page_channels_tree_view
		# _plot_page_channels_tree_store

		
		checkbox_title = Gtk.CellRendererToggle()
		checkbox_title.connect("toggled", self.plotting_page_on_channel_toggle, self._plot_page_channels_tree_store)
		column = Gtk.TreeViewColumn("Select", checkbox_title)
		self._plot_page_channels_tree_view.append_column(column)

		text_title = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Label", text_title, markup=1)
		self._plot_page_channels_tree_view.append_column(column)



		for device_name, device in self._devices.items():

			device_iter = self._plot_page_channels_tree_store.append( None, [Gtk.CheckButton(device.label()), device.label(), "Device", device.name(), device.name()] )

			for channel_name, channel in device.channels().items():
				
				if channel.mode() == "read" or channel.mode() == "both" and ( channel.data_type() == float or channel.data_type() == int ):
					channel_iter = self._plot_page_channels_tree_store.append( device_iter, [Gtk.CheckButton(channel.label()), channel.label(), "Channel", device.name(), channel.name()] )

		
		

		
		


		self._builder.get_object("plotting_scrolled_window").add(self._plot_page_channels_tree_view)

		self._plot_page_channels_tree_view.show()

		self._main_window.show_all()

		

	'''
	def setup_plotting_page(self):

		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self._builder.get_object("plots_box").add(box)

		grid = Gtk.Grid(column_spacing=30, row_spacing=150, margin=100)
		grid.set_column_homogeneous(True)
		grid.set_row_homogeneous(True)

		box.add(grid)		

		grid.show_all()
		self._builder.get_object("plots_box").show_all()
	'''



	def setup_settings_page(self):

		scrolled_window = self._builder.get_object("settings_scrolled_window")

		
		
		# for device_name, device in self._devices.items():

		# 	device_iter = self._settings_page_tree_store.append(None, [device.label(), "Device", "edit_device", device.name(), device.name()])

		# 	for channel_name, channel in device.channels().items():
		# 		channel_iter = self._settings_page_tree_store.append(device_iter, [channel.label(), "Channel", "edit_channel", channel.name(), device.name()])

		# 	channel_iter = self._settings_page_tree_store.append(device_iter, ["<b>[ Add a New Channel ]</b>", "", "add_new_channel", device.name(), device.name()])

		device_iter = self._settings_page_tree_store.append(None, ["<b>[ Add a New Device ]</b>", "", "add_new_device", "", ""])
		

		title = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Label", title, markup=0)
		self._settings_tree_view.append_column(column)

		column = Gtk.TreeViewColumn("Object Type", title, markup=1)
		self._settings_tree_view.append_column(column)


		select = self._settings_tree_view.get_selection()
		select.connect("changed", self.device_settings_tree_selection_callback)

		scrolled_window.add(self._settings_tree_view)

		
		self._main_window.show_all()


	def get_plotting_canvas(self, title=""):
		fig = Figure(figsize=(1,1), dpi=60)
		ax = fig.add_subplot(111)

		n = 1000
		xsin = np.linspace(-np.pi, np.pi, n, endpoint=True)
		xcos = np.linspace(-np.pi, np.pi, n, endpoint=True)
		ysin = np.sin(xsin)
		ycos = np.cos(xcos)

		sinwave = ax.plot(xsin, ysin, color='black', label='sin(x)')
		coswave = ax.plot(xcos, ycos, color='black', label='cos(x)', linestyle='--')

		ax.set_xlim(-np.pi,np.pi)
		ax.set_ylim(-1.2,1.2)

		ax.fill_between(xsin, 0, ysin, (ysin - 1) > -1, color='blue', alpha=.3)
		ax.fill_between(xsin, 0, ysin, (ysin - 1) < -1, color='red',  alpha=.3)
		ax.fill_between(xcos, 0, ycos, (ycos - 1) > -1, color='blue', alpha=.3)
		ax.fill_between(xcos, 0, ycos, (ycos - 1) < -1, color='red',  alpha=.3)

		ax.legend(loc='upper left')

		ax = fig.gca()
		ax.spines['right'].set_color('none')
		ax.spines['top'].set_color('none')
		ax.xaxis.set_ticks_position('bottom')
		ax.spines['bottom'].set_position(('data',0))
		ax.yaxis.set_ticks_position('left')
		ax.spines['left'].set_position(('data',0))

		fig.tight_layout(pad=0.5, h_pad=0.5, w_pad=0.1)

		canvas = FigureCanvas(fig)

		ax.set_title(title)

		canvas.resize(5, 5)



		return canvas


	



	def reinitialize(self):
		for device_name, device in self._devices.items():
			if not device.initialized():
				device.initialize()

		self.set_widget_connections()

		self.setup_communication_threads()

		self._main_window.show_all()


	def main_quit(self, widget):
		"""
		Shuts down the program (and threads) gracefully.
		:return:
		"""

		self._main_window.destroy()
		self.shut_down_communication_threads()

		self.shut_down_procedure_threads()

		Gtk.main_quit()

		return 0


	def shut_down_procedure_threads(self):
		self._keep_critical_procedure_threads_running = False
		self._keep_procedure_thread_running = False


	def shut_down_communication_threads(self):
		"""
		:return:
		"""
		self._keep_communicating = False

		return 0

	def run(self):
		"""
		:return:
		"""
		self.initialize()

		# --- Show the GUI --- #
		self._main_window.maximize()
		self._main_window.show_all()

		Gtk.main()

		return 0

	def statusbar_changed_callback(self, statusbar, context_id, text):
		"""
		Callback that handles what happens when a message is pushed in the
		statusbar
		"""

		timestr = time.strftime("%d %b, %Y, %H:%M:%S: ", time.localtime())

		self._log_textbuffer.insert(self._log_textbuffer.get_end_iter(), timestr + text + "\n")

		return 0


	def dummy_update(self):
		pass

	def update_gui(self, channel):
		"""
		Updates the GUI. This is called from the communication threads through idle_add()
		:return:
		"""
		# Update the polling rate (frequency) for this arduino:
		arduino_id = channel.get_arduino_id()
		count = self._communication_threads_poll_count[arduino_id]

		if count >= 10:

			elapsed = time.time() - self._communication_threads_start_time[arduino_id]
			frequency = self._communication_threads_poll_count[arduino_id] / elapsed

			self._communication_threads_start_time[arduino_id] = time.time()
			self._communication_threads_poll_count[arduino_id] = 0

			self._arduino_status_bars[arduino_id].set_value(frequency)


		# If display on overview page is desired, update:
		if channel.get_parent_device().is_on_overview_page():
			# if count == 9:
			# 	print "Updating", channel.name(), channel.get_value()
			channel.get_overview_page_display().set_value(channel.get_value())

		return 0


if __name__ == "__main__":

	control_system = MIST1ControlSystem()

	# Setup data logging.
	current_time = time.strftime('%a-%d-%b-%Y_%H %M %S-EST', time.localtime())
	control_system.register_data_logging_file(filename="log/{}.hdf5".format(current_time))

	# Generate a device.
	# Each device is connected to a single arduino, several devices can be connected to the
	# same Arduino, but never several arduinos to a single device!

	# Aashish => 2cc580d6-fa29-44a7-9fec-035acd72340e
	# Actual Interlock Box => 49ffb802-50c5-4194-879d-20a87bcfc6ef

	interlock_box_device = Device("interlock_box", arduino_id="2cc580d6-fa29-44a7-9fec-035acd72340e", label="Interlock Box")
	interlock_box_device.set_overview_page_presence(True)

	
	# Add channels to the interlock box device.

	# Flow meters. x5.
	for i in range(5):
	# for i in range(1):
		ch = Channel(name="flow_meter#{}".format(i + 1), label="Flow Meter {}".format(i + 1),
					 message_header="flow_meter#" + str(i + 1),
					 upper_limit=1,
					 lower_limit=0,
					 data_type=int,
					 mode="read",
					 unit="Hz",
					 display_order=(11 - i))

		interlock_box_device.add_channel(ch)

	# Microswitches. x2.
	for i in range(2):
		ch = Channel(name="micro_switch#{}".format(i + 1), label="Micro Switch {}".format(i + 1),
					message_header="micro_switch#{}".format(i + 1),
					upper_limit=1,
					lower_limit=0,
					data_type=bool,
					mode="read",
					display_order=(11 - 5 - i))

		interlock_box_device.add_channel(ch)
	
	# Solenoid valves. x2.
	for i in range(2):
		ch = Channel(name="solenoid_valve#{}".format(i + 1), label="Solenoid Valve {}".format(i + 1),
					message_header="solenoid_valve#{}".format(i + 1),
					upper_limit=1,
					lower_limit=0,
					data_type=bool,
					mode="write",
					display_order=(11 - 5 - 2 - i))

		interlock_box_device.add_channel(ch)

	# Vacuum Valves. x2.
	for i in range(2):
		ch = Channel(name="vacuum_valve#{}".format(i + 1), label="Vacuum Valve {}".format(i + 1),
					message_header="vacuum_valve#{}".format(i + 1),
					upper_limit=1,
					lower_limit=0,
					data_type=bool,
					mode="read",
					display_order=(11 - 5 - 2 - 2 - i))

		interlock_box_device.add_channel(ch)

	# Add all our devices to the control system.
	
	control_system.add_device(interlock_box_device)



	'''
	# # This is for adding procedures. 
	# # TODO: Needs more work. Work on this later.
	interlock_shutdown_conditions = [ (lambda x: x > 100, interlock_box_device.channels()['flow_meter#1'] ) ]

	def action_function(some_string, some_int, some_channel):
		print "Some string", some_string
		print "Some int", some_int
		print "Some channel", some_channel.get_value()


	interlock_shutdown_action = [ (action_function, dict(some_string="hey there", some_int=42, some_channel=interlock_box_device.channels()['flow_meter#1'])) ]

	interlock_procedure = Procedure(name="interlock_proc", conditions=interlock_shutdown_conditions, actions=interlock_shutdown_action)

	control_system.add_procedure(interlock_procedure)
	'''


	'''
	# # This is for reading / writing from json files.
	# interlock_box_device.write_json("devices/interlock.json")

	# interlock_box = Device.load_from_json("devices/interlock.json")

	# control_system.add_device(interlock_box)
	'''

	# AASHISH Interlock Box => 2cc580d6-fa29-44a7-9fec-035acd72340e
	# AASHISH Ion Gauge => 41b70a36-a206-41c5-b743-1e5b8429b9a1
	# Actual Ion Gauge Controller Arduino => cf436e6b-ba3d-479a-b221-bc387c37b858

	ion_gauge = Device("ion_gauge", arduino_id="41b70a36-a206-41c5-b743-1e5b8429b9a1", label="Ion Gauge")
	ion_gauge.set_overview_page_presence(True)

	for i in range(2):
		ch = Channel(name="gauge_state#{}".format(i + 1), label="Gauge State {}".format(i + 1),
					 message_header="gauge_state#" + str(i + 1),
					 upper_limit=1,
					 lower_limit=0,
					 data_type=bool,
					 mode="read",
					 display_order=(4 - i))

		ion_gauge.add_channel(ch)

	for i in range(2):
		ch = Channel(name="gauge_pressure#{}".format(i + 1), label="Gauge Pressure {}".format(i + 1),
					 message_header="gauge_pressure#" + str(i + 1),
					 upper_limit=1000,
					 lower_limit=0,
					 data_type=float,
					 mode="read",
					 unit="Torr",
					 display_order=(4 - i),
					 displayformat=".2e")

		ion_gauge.add_channel(ch)

	control_system.add_device(ion_gauge)

	



	'''
	# # This is for reading / writing from json files.

	# ion_gauge.write_json("devices/ion_gauge.json")

	# ion_gauge = Device.load_from_json("devices/ion_gauge.json")
	
	# control_system.add_device(ion_gauge)
	'''
	

	# Run the control system, this has to be last as it does all the initializations and adding to the GUI.
	control_system.run()


