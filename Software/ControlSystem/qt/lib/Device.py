import json
import time

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QFrame
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject

from .Channel import Channel
from gui.widgets.EntryForm import EntryForm

class DeviceWidget(QWidget):

    def __init__(self, device):
        super().__init__()
        
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        gb = QGroupBox(device.label)
        self._layout.addWidget(gb)
        self._layout.addStretch()

        self._gblayout = QVBoxLayout()
        gb.setLayout(self._gblayout)

    def show_error_message(self, message=''):
        fm = QFrame()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        fm.setLayout(vbox)
        txtError = QLabel('<font color="red">{}</font>'.format(message))
        txtError.setWordWrap(True)
        txtRetry = QLabel('Retrying in 5 seconds...')
        vbox.addWidget(txtError)
        vbox.addWidget(txtRetry)
        self._layout.insertWidget(0, fm)
        self.setEnabled(False)

    def hide_error_message(self):
        wdg = self._layout.takeAt(0).widget()
        wdg.deleteLater()
        self.setEnabled(True)

    @property
    def gblayout(self):
        return self._gblayout
    
class Device(QObject):

    _sig_entry_form_ok = pyqtSignal(object, dict)
    _sig_delete = pyqtSignal(object)

    def __init__(self, name='', device_id='', label='', channels=None, 
                 driver='Arduino', overview_order=-1):
        super().__init__()

        self._name = name
        self._label = label

        self._channels = {}  # This is a dictionary of channels with their names as keys.
        if channels is not None:
            self._channels = channels

        self._device_id = device_id
        self._driver = driver

        self._parent = None
        self._locked = False

        self._pages = ['overview']
        self._overview_order = overview_order

        self._error_message = ''
        self._hasError = False

        self._entry_form = EntryForm(self._label, '', self.user_edit_properties(), self)
        self._entry_form.sig_save.connect(self.save_changes)
        self._entry_form.sig_delete.connect(self.delete)

        self._initialized = False

    @property
    def initialized(self):
        return self._initialized

    def initialize(self):

        # create gui representation
        self._overview_widget = DeviceWidget(self)
        self._gblayout = self._overview_widget.gblayout

        self._initialized = True
        self._entry_form.add_delete_button()

    def reset_entry_form(self):
        self._entry_form.properties = self.user_edit_properties()
        self._entry_form.reset()

    @pyqtSlot(dict)
    def save_changes(self, newvals):
        """ Validates the user data entered into the device's entry form """
        validvals = {}
        for prop_name, val in newvals.items():
            if prop_name == 'overview_order':
                try:
                    value = int(val)
                except:
                    print('Display order must be an int')
                    return
            else:
                if val != '':
                    value = val
                else:
                    print('No value entered for {}.'.format(
                        self.user_edit_properties()[prop_name]['display_name']))
                    return

            validvals[prop_name] = value

        self._sig_entry_form_ok.emit(self, validvals)

    @pyqtSlot()
    def delete(self):
        self._sig_delete.emit(self)

    @property
    def sig_entry_form_ok(self):
        return self._sig_entry_form_ok

    @property
    def sig_delete(self):
        return self._sig_delete

    @staticmethod
    def driver_list():
        return ['Arduino', 'RS485', 'FT232R', 'Teensy', 'Prolific']

    #@staticmethod
    def user_edit_properties(self):
        """ Returns list of properties that should be user-editable 
            key name must match a property of this class """
            
        return {
                'name': {
                    'display_name': 'Name', 
                    'entry_type': 'text',
                    'value': self._name,
                    'display_order': 1
                    },
                'device_id': {
                    'display_name': 'Device ID', 
                    'entry_type': 'text',
                    'value': self._device_id,
                    'display_order': 2
                    },
                'label': {
                    'display_name': 'Label', 
                    'entry_type': 'text',
                    'value': self._label,
                    'display_order': 3
                    },
                'driver': {
                    'display_name': 'Driver', 
                    'entry_type': 'combo',
                    'value': self._driver,
                    'defaults': self.driver_list(),
                    'display_order': 4
                    },
                'overview_order': {
                    'display_name': 'Display Order', 
                    'entry_type': 'text',
                    'value': self._overview_order,
                    'display_order': 5
                    },
                }

    @property
    def entry_form(self):
        return self._entry_form.widget

    def update(self):
        # reorder the channels
        if not self._initialized:
            return

        while self._gblayout.count():
            child = self._gblayout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

        chlist = [ch for chname, ch in reversed(sorted(self._channels.items(), 
                                                        key=lambda x: x[1].display_order))]

        for idx, ch in enumerate(chlist):
            ch._overview_widget.setParent(None)

        for idx, ch in enumerate(chlist):
            self._gblayout.insertWidget(idx, ch._overview_widget)

    @property
    def error_message(self):
        return self._error_message

    @error_message.setter
    def error_message(self, value):
        self._error_message = value

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    @property
    def driver(self):
        return self._driver
    
    @driver.setter
    def driver(self, value):
        self._driver = value

    @property
    def parent(self):
        return parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def label(self):
        return self._label
    
    @label.setter
    def label(self, value):
        self._label = value
        if not self._initialized:
            return

        if self._gblayout.parent().title() != self._label:
            self._gblayout.parent().setTitle(self._label)
            for channel_name, channel in self.channels.items():
                channel.update()

    @property
    def pages(self):
        return self._pages

    @property
    def overview_order(self):
        return self._overview_order

    @overview_order.setter
    def overview_order(self, value):
        self._overview_order = value

    def add_page(self, value):
        self._pages.append(value)

    @property
    def channels(self):
        return self._channels

    def get_channel_by_name(self, channel_name):
        try:
            return self._channels[channel_name]
        except:
            return None

    def add_channel(self, channel):
        channel.initialize()
        channel.device_id = self._device_id
        channel.parent_device = self
        self._channels[channel.name] = channel
        self.update()

    def lock(self, message=''):
    """ Disable the device, and display an error message """
        self._error_message = message
        if not self._locked:
            self._overview_widget.show_error_message(self._error_message)
            self._locked = True

    def unlock(self):
        if self._locked:
            self._overview_widget.hide_error_message()
            self._locked = False

    @property
    def locked(self):
        return self._locked

    def get_json(self):
        """ Gets a serializable representation of this device """
        properties = {'name': self._name,
                      'label': self._label,
                      'device_id': self._device_id,
                      'driver': self._driver,
                      'channels': {},
                      'overview_order': self._overview_order
                      }

        for channel_name, channel in self._channels.items():
            properties['channels'][channel_name] = channel.get_json()

        return properties #json.dumps(properties)

    def write_json(self, filename):
        myjson = self.get_json()

        with open(filename, "wb") as f:
            f.write(myjson)

    @staticmethod
    def load_from_json(string):
        with open(filename, "rb") as f:
            data = json.load(f)

        filtered_params = {}
        for key, value in data.items():
            if not key == "channels":
                filtered_params[key] = value

        device = Device(**filtered_params)

        for channel_name in data['channels']:
            channel_json = data['channels'][channel_name]
            ch = Channel.load_from_json(channel_json)

            device.add_channel(ch)

        return device
