#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Thomas Wester <twester@mit.edu>
# Handles dialog and widget creation

import time
import copy
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, \
                            QGroupBox, QLineEdit, QFrame, QLabel, \
                            QRadioButton, QScrollArea, QPushButton, \
                            QWidget, QSizePolicy, QAction, QTreeWidgetItem, \
                            QComboBox
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont

import pyqtgraph as pg
from pyqtgraph.widgets.RemoteGraphicsView import RemoteGraphicsView

from .ui_MainWindow import Ui_MainWindow
from .dialogs.PlotChooseDialog import PlotChooseDialog 
from .dialogs.ProcedureDialog import ProcedureDialog 
from .dialogs.AboutDialog import AboutDialog 
from lib.Device import Device
from lib.Channel import Channel
from lib.Procedure import Procedure

class MainWindow(QMainWindow):
    # signal to be emitted to main program when plots change on plotting page
    sig_plots_changed = pyqtSignal(dict)

    #signal to be emitted when procedures change
    sig_procedures_changed = pyqtSignal(dict)

    # signal to be emitted when device/channel is changed
    sig_device_channel_changed = pyqtSignal(object, dict)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # aliases
        self._statusbar = self.ui.statusBar
        self._messagelog = self.ui.txtMessageLog
        self._overview = self.ui.fmOverview
        self._plots = self.ui.fmPlots
        self._pinnedplot = self.ui.pltPinned
        self._gbpinnedplot = self.ui.gbPinnedPlot
        self._tabview = self.ui.tabMain
        self._btnquit = self.ui.btnQuit
        self._btnplotchoose = self.ui.btnSetupDevicePlots
        self._btnaddprocedure = self.ui.btnAddProcedure

        # add a right-aligned About tool bar button
        spc = QWidget()
        spc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spc.setVisible(True)
        self.ui.toolBar.addWidget(spc)
        self._btnAbout = QAction('About', None)
        self.ui.toolBar.addAction(self._btnAbout)

        # dialog connections
        self._btnplotchoose.clicked.connect(self.show_PlotChooseDialog)
        self._btnaddprocedure.clicked.connect(self.show_ProcedureDialog)
        self._btnAbout.triggered.connect(self.show_AboutDialog)

        # tab changes
        self._current_tab = 'main'
        self._tabview.currentChanged.connect(self.tab_changed)

        ## set up containers
        self._overview_layout = QHBoxLayout()
        self._overview.setLayout(self._overview_layout) 
        self._overview_layout.addStretch()
        #self._overview.setLayoutDirection(Qt.RightToLeft)

        self._gbox = QGridLayout()
        self._plots.setLayout(self._gbox)

        # settings page
        self.ui.treeDevices.setHeaderLabels(['Label', 'Type'])
        self.ui.treeDevices.currentItemChanged.connect(self.on_settings_row_changed)
        self.ui.btnExpand.clicked.connect(self.ui.treeDevices.expandAll)
        self.ui.btnCollapse.clicked.connect(self.ui.treeDevices.collapseAll)
        self._devvbox = QVBoxLayout()
        self.ui.fmDeviceSettings.setLayout(self._devvbox)

        # local copies of data
        self._overview_devices = {}
        self._settings_devices = {}
        self._plotted_channels = {}
        self._procedures = {}

        self._prevproc = None

    @property
    def current_tab(self):
        return self._current_tab

    def tab_changed(self):
        tabName = self._tabview.tabText(self._tabview.currentIndex())
        if tabName == 'Overview':
            self._current_tab = 'main'
        elif tabName == 'Devices':
            self._current_tab = 'devices'
        elif tabName == 'Plotting':
            self._current_tab = 'plots'

    def update_overview(self, devices):
        #self.clearLayout(self._overview_layout)
        for device_name, device in devices.items():
            if 'overview' in device.pages and device._overview_widget.parent() == None:
                self._overview_layout.insertLayout(0, device._overview_widget)
        
    def set_polling_rate(self, text):
        self.ui.lblServPoll.setText('Server polling rate: ' + text + ' Hz')

    def status_message(self, text):
        self._statusbar.showMessage(text)
        self._messagelog.append(time.strftime('[%Y-%m-%d %H:%M:%S] ', time.localtime()) + text)

    def show_PlotChooseDialog(self):
        devdict = {}
        for devname, data in self._overview_devices.items():
            devdict[devname] = data['device']

        _plotchoosedialog = PlotChooseDialog(devdict, self._plotted_channels)
        # dialog returns a tuple (bool, list), bool is true if closed via 'Done' button
        # list contains channel objects to be plotted
        accept, chs = _plotchoosedialog.exec_()
        if accept:
            # update plotted channels
            newplottedchs = {}
            for ch in chs:
                dev = ch.parent_device
                newplottedchs[(dev.name, ch.name)] = {'channel': ch, 
                                                      'curve': None,
                                                      'btnPin': None,
                                                      'color' : 'r'}
            # TODO need to figure out a nice way to not redraw plots 
            # if they haven't changed.
            if newplottedchs != self._plotted_channels:
                self._plotted_channels = newplottedchs
                self.update_plots()

    @pyqtSlot()
    @pyqtSlot(Procedure)
    # can be called with no arguments, or a Procedure argument
    # a bool argument gets passed from the button click without the decorators, which we don't want
    def show_ProcedureDialog(self, proc=None):
        devdict = {}
        for devname, data in self._overview_devices.items():
            devdict[devname] = data['device']

        _proceduredialog = ProcedureDialog(devdict, self._procedures.keys(), proc)
        accept, rproc = _proceduredialog.exec_()

        if rproc is not None:
            if proc is not None:
                # if we edited a procedure delete the old version before adding the new one
                del self._procedures[proc.name]
            self._procedures[rproc.name] = rproc 
            self.update_procedures()

    def update_procedures(self):
        # Add procedures to the procedures tab
        self.clearLayout(self.ui.vboxProcedures)
        for name, proc in self._procedures.items():
            title = ''
            if proc.critical:
                title = '(Critical) {}'.format(proc.name)
            else:
                title = proc.name
            gb = QGroupBox(title)
            vbox = QVBoxLayout()
            gb.setLayout(vbox)
            lblProc = QLabel(proc.info)
            vbox.addWidget(lblProc)
            hbox = QHBoxLayout()
            hbox.addStretch()
            btnEdit = QPushButtonProc('Edit', proc)
            btnDelete = QPushButtonProc('Delete', proc)
            btnEdit.clickedX.connect(self.edit_procedure)
            btnDelete.clickedX.connect(self.delete_procedure)
            hbox.addWidget(btnEdit)
            hbox.addWidget(btnDelete)
            vbox.addLayout(hbox)

            self.ui.vboxProcedures.addWidget(gb)

        self.ui.vboxProcedures.addStretch()

    @pyqtSlot(Procedure)
    def delete_procedure(self, proc):
        del self._procedures[proc.name]
        self.update_procedures()

    @pyqtSlot(Procedure)
    def edit_procedure(self, proc):
        self.show_ProcedureDialog(proc = proc)

    def show_AboutDialog(self):
        _aboutdialog = AboutDialog()
        _aboutdialog.exec_()

    def update_plots(self):
        self.clearLayout(self._gbox)
        row = 0
        col = 0
        for names, data in self._plotted_channels.items():
            ch = data['channel']
            chbox = QGroupBox(ch.parent_device.label + " / " + ch.label)
            vbox = QVBoxLayout()
            chbox.setLayout(vbox)
            self._gbox.addWidget(chbox, row, col)
            pltBox = pg.PlotWidget()
            vbox.addWidget(pltBox)
            self._plotted_channels[(ch.parent_device.name, ch.name)]['curve'] = pltBox.plot(pen=data['color'])
            pinbutton = QPushButtonX('Pin', ch)
            self._plotted_channels[(ch.parent_device.name, ch.name)]['btnPin'] = pinbutton.clickedX
            vbox.addWidget(pinbutton)
            row += 1
            if row == 2:
                row = 0
                col += 1
        self.sig_plots_changed.emit(self._plotted_channels)

    def update_device_settings(self, devices):
        self.ui.treeDevices.clear()
        for device_name, device in devices.items():
            devrow = QTreeWidgetItem(self.ui.treeDevices)
            devrow.setText(0, device.label)
            devrow.setText(1, 'Device')
            self._settings_devices[device.name] = {'device': device, 'row': devrow, 'channels': {}}
            for chname, ch in reversed(sorted(device.channels.items(), key=lambda x: x[1].display_order)):
                chrow = QTreeWidgetItem(devrow)
                chrow.setText(0, ch.label)
                chrow.setText(1, 'Channel')
                self._settings_devices[device.name]['channels'][ch.name] = {'channel': ch, 'row': chrow}
            newchrow = QTreeWidgetItem(devrow)
            newchrow.setText(0, '[Add a new Channel]')
            #newchrow.setText(1, 'Channel')

        newdevrow = QTreeWidgetItem(self.ui.treeDevices)
        newdevrow.setText(0, '[Add a new Device]')
        #newdevrow.setText(1, 'Device')

        self.ui.treeDevices.expandAll()

    def on_settings_row_changed(self, item):
        if item == None:
            # if nothing is selected, do nothing
            return

        self.clearLayout(self._devvbox)
        # recover the associated object to change
        obj = None
        parent = None

        for device_name, device_data in self._settings_devices.items():
            # are we editing an existing device/channel?
            if device_data['row'] == item:
                obj = device_data['device']
                break
            else:
                for channel_name, channel_data in device_data['channels'].items():
                    if channel_data['row'] == item:
                        obj = channel_data['channel']
                        parent = device_data['device']
                        break

        if (obj, parent) == (None, None):
            # adding a new device or channel
            if 'channel' in item.text(0).lower():
                for device_name, device_data in self._settings_devices.items():
                    if device_data['row'] == item.parent():
                            parent = device_data['device']
                            break


        if parent is None: #type(obj) == Device or 'device' in item.text(0).lower():
            # set up device entry form
            label = ''
            name = ''
            ardid = ''

            if obj is not None:
                label = obj.label
                name = obj.name
                ardid = obj.arduino_id
            else:
                label = 'New Device'

            lblTitle = QLabel(label)
            font = QFont()
            font.setPointSize(14)
            lblTitle.setFont(font)
            self._devvbox.addWidget(lblTitle)
            gbox = QGridLayout()
            
            lblArdId = QLabel('Arduino ID')
            lblLabel = QLabel('Label')
            lblName = QLabel('Name')
            
            txtArdId = QLineEdit(ardid)
            txtLabel = QLineEdit(label)
            txtName = QLineEdit(name)

            gbox.addWidget(lblName, 0, 0)
            gbox.addWidget(txtName, 0, 1)
            gbox.addWidget(lblArdId, 1, 0)
            gbox.addWidget(txtArdId, 1, 1)
            gbox.addWidget(lblLabel, 2, 0)
            gbox.addWidget(txtLabel, 2, 1)

            self._devvbox.addLayout(gbox)

            hbox = QHBoxLayout()
            hbox.addStretch()
            if obj is not None:
                btnSave = QPushButtonObj('Save Changes', obj)
            else:
                btnSave = QPushButtonObj('Save Changes', 'device')
            btnSave.clickedX.connect(self.on_save_changes_click)
            hbox.addWidget(btnSave)
            hbox.addStretch()

            self._devvbox.addLayout(hbox)

            self._devvbox.addStretch()
        else: # type(obj) == Channel or 'channel' in item.text(0).lower():
            # set up channel entry form
            title = '{}/{}'.format(parent.label,'New Channel')
            if obj is not None:
                title = '{}/{}'.format(obj.parent_device.label, obj.label)
            lblTitle = QLabel(title)
            font = QFont()
            font.setPointSize(14)
            lblTitle.setFont(font)
            self._devvbox.addWidget(lblTitle)
            gbox = QGridLayout()
            
            lblMode = QLabel('Read/Write')
            lblType = QLabel('Data Type')
            lblUnit = QLabel('Unit')
            lblMinVal = QLabel('Lower Limit')
            lblMaxVal = QLabel('Upper Limit')
            lblLabel = QLabel('Label')
            lblName = QLabel('Name')
            
            cbType = QComboBox()
            cbType.addItems(['Int', 'Bool', 'Float'])
            cbMode = QComboBox()
            cbMode.addItems(['Read', 'Write', 'Both'])

            unit = ''
            minval = ''
            maxval = ''
            label = ''
            name = ''
            if obj is not None:
                if obj.mode == 'read':
                    cbMode.setCurrentIndex(0)
                elif obj.mode == 'write':
                    cbMode.setCurrentIndex(1)
                else:
                    cbMode.setCurrentIndex(2)

                if obj.data_type == int:
                    cbType.setCurrentIndex(0)
                elif obj.data_type == bool:
                    cbType.setCurrentIndex(1)
                else:
                    cbType.setCurrentIndex(2)

                unit = obj.unit
                minval = str(obj.lower_limit)
                maxval = str(obj.upper_limit)
                label = obj.label
                name = obj.name

            txtUnit = QLineEdit(unit)
            txtMinVal = QLineEdit(minval)
            txtMaxVal = QLineEdit(maxval)
            txtLabel = QLineEdit(label)
            txtName = QLineEdit(name)

            gbox.addWidget(lblName, 0, 0)
            gbox.addWidget(txtName, 0, 1)
            gbox.addWidget(lblLabel, 1, 0)
            gbox.addWidget(txtLabel, 1, 1)
            gbox.addWidget(lblUnit, 2, 0)
            gbox.addWidget(txtUnit, 2, 1)
            gbox.addWidget(lblMinVal, 3, 0)
            gbox.addWidget(txtMinVal, 3, 1)
            gbox.addWidget(lblMaxVal, 4, 0)
            gbox.addWidget(txtMaxVal, 4, 1)
            gbox.addWidget(lblType, 5, 0)
            gbox.addWidget(cbType, 5, 1)
            gbox.addWidget(lblMode, 6, 0)
            gbox.addWidget(cbMode, 6, 1)

            self._devvbox.addLayout(gbox)

            hbox = QHBoxLayout()
            hbox.addStretch()
            if obj is not None:
                btnSave = QPushButtonObj('Save Changes', obj)
            else:
                btnSave = QPushButtonObj('Save Changes', ('channel', parent))
            btnSave.clickedX.connect(self.on_save_changes_click)
            hbox.addWidget(btnSave)
            hbox.addStretch()

            self._devvbox.addLayout(hbox)

            self._devvbox.addStretch()
            if obj is not None:
                hbox = QHBoxLayout()
                hbox.addStretch()
                btnDel = QPushButtonObj('Delete Channel', obj)
                hbox.addWidget(btnDel)
                hbox.addStretch()
                self._devvbox.addLayout(hbox)

    def on_save_changes_click(self, obj):
        newobj = None
        newvals = {}
        if type(obj) == Device or (type(obj) == str and 'device' in obj.lower()):
            # TODO This is hard-coded to avoid passing references to all the controls around
            # probably not the best solution.

            # order is: name, arduino_id, label -> (1, 3, 5)
            gbox = self._devvbox.itemAt(1).layout()
            name = gbox.itemAt(1).widget().text()
            label = gbox.itemAt(5).widget().text()
            
            ard_id = gbox.itemAt(3).widget().text()

            if type(obj) == Device:
                # we are modifying a device
                newobj = obj
                newvals = {'name': name, 'label': label, 'arduino_id': ard_id}
            else:
                # we are adding a new device. No need to set newvals
                newobj = Device(name, ard_id, label) 

        else:
            gbox = self._devvbox.itemAt(1).layout()

            # order is: name, label, unit, lower, upper, type, mode
            name = gbox.itemAt(1).widget().text()
            label = gbox.itemAt(3).widget().text()
            unit = gbox.itemAt(5).widget().text()

            cbType = gbox.itemAt(11).widget()
            # int, bool, float
            data_type = None
            if cbType.currentIndex() == 0:
                data_type = int
            elif cbType.currentIndex() == 1:
                data_type = bool
            else:
                data_type = float

            try:
                lower_limit = data_type(gbox.itemAt(7).widget().text())
                upper_limit = data_type(gbox.itemAt(9).widget().text())
            except:
                print('bad values for limits')
                return

            cbMode = gbox.itemAt(13).widget()
            # read, write, both
            mode = ''
            if cbMode.currentIndex() == 0:
                mode = 'read'
            elif cbMode.currentIndex() == 1:
                mode = 'write'
            else:
                mode = 'both'

            if type(obj) == Channel:
                # modifying a channel. Set newobj and newvals
                newobj = obj
                newvals = {'label': label, 'unit': unit, 'data_type': data_type,
                           'lower_limit': lower_limit, 'upper_limit': upper_limit,
                           'mode': mode, 'name': name}
            else:
                # adding a new channel, only set newobj
                parent = obj[1]
                newobj = Channel(name, label, upper_limit, lower_limit, data_type, unit)
                newobj.parent_device = parent

        self.clearLayout(self._devvbox)
        #self.clearLayout(self._overview_layout)
        self.sig_device_channel_changed.emit(newobj, newvals)

    def clearLayout(self ,layout):
        """ Recursively removes all items from a QLayout """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            if child.layout():
                self.clearLayout(child)

# ----- Custom Controls ----- #
class QLineEditX(QLineEdit):
    """ QLineEdit which returns a dict of channel info on returnPressed """
    returnPressedX = pyqtSignal(dict)

    def __init__(self, channel):
        super().__init__()
        self.ch = channel
        self.setText(str(self.ch.value))
        self.returnPressed.connect(self.on_return_pressed)

    @pyqtSlot()
    def on_return_pressed(self):
        try:
            value = self.ch.data_type(self.text()) #will fail here if input is bad
            if value != max(self.ch.lower_limit, min(value, self.ch.upper_limit)):
                raise ValueError('Value not within channel limits')
            data = {'channel': self.ch,
                    'value': value, 
                    'emitter':self.returnPressedX}
            self.returnPressedX.emit(data)
            self.setText(str(value))
        except:
            print("bad input")

class QPushButtonX(QPushButton):
    """ QPushButton which returns a dict of channel info on clicked """
    clickedX = pyqtSignal(tuple)

    def __init__(self, text, channel):
        super().__init__()
        self.ch = channel
        self.setText(text)
        self.clicked.connect(self.on_clicked)

    @pyqtSlot()
    def on_clicked(self):
        data = (self.ch.parent_device, self.ch)
        self.clickedX.emit(data)

class QPushButtonObj(QPushButton):
    """ QPushButton which returns an object on click """
    clickedX = pyqtSignal(object)

    def __init__(self, text, obj):
        super().__init__()
        self.obj = obj
        self.setText(text)
        self.clicked.connect(self.on_clicked)

    @pyqtSlot()
    def on_clicked(self):
        self.clickedX.emit(self.obj)

class QPushButtonProc(QPushButton):
    """ QPushButton which returns a dict of channel info on clicked """
    clickedX = pyqtSignal(Procedure)

    def __init__(self, text, proc):
        super().__init__()
        self._proc = proc
        self.setText(text)
        self.clicked.connect(self.on_clicked)

    @pyqtSlot()
    def on_clicked(self):
        data = self._proc
        self.clickedX.emit(data)

class QRadioButtonX(QRadioButton):
    """ QRadioButton which returns a dict of channel info on toggled """
    toggledX = pyqtSignal(dict)

    def __init__(self, text, channel):
        super().__init__()
        self.ch = channel
        self.setText(text)
        self.toggled.connect(self.on_toggled)

    def on_toggled(self):
        value = float(self.isChecked())
        data = {'channel': self.ch,
                'value' : value,
                'emitted': self.toggledX}
        self.toggledX.emit(data)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()

    sys.exit(app.exec_())
