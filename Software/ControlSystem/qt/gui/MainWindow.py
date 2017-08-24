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
    sig_device_channel_changed = pyqtSignal()

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
        self._overview.setLayoutDirection(Qt.RightToLeft)
        self._overview_layout.addStretch()

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

    def add_device_to_overview(self, device):
        if device in [x['device'] for _a, x in self._overview_devices.items()]:
            return

        # create group box for this device, add it to overview frame
        vwrap = QVBoxLayout()
        devbox = QGroupBox(device.label)
        devbox.setMaximumWidth(250)
        devbox.setLayoutDirection(Qt.LeftToRight)
        # add groupbox to first row, nth column
        vwrap.addWidget(devbox)
        vwrap.addStretch()
        self._overview_layout.addLayout(vwrap) #, Qt.AlignLeft)
        self._overview_layout.setAlignment(devbox, Qt.AlignLeft)
        vbox = QVBoxLayout()
        devbox.setLayout(vbox)

        self._overview_devices[device.arduino_id] = {'device': device, 
                                                     'groupbox': devbox,
                                                     'layout': vbox}

        # dict of signals needed from these controls by the main control system
        emitters = {} 

        # dict of QTextEdits to have their text set by the main control system (read values)
        readboxes = {}

        for chname, ch in reversed(sorted(device.channels.items(), key=lambda x: x[1].display_order)):
            # create frame for channel info
            gb = QGroupBox(ch.label)

            if ch.data_type == float:
                # set the group box to vertical layout
                vl = QVBoxLayout()
                gb.setLayout(vl)

                if ch.mode == 'write' or ch.mode == 'both':
                    # create a row with a text box, add it to group box
                    row = QFrame()
                    hl = QHBoxLayout()
                    hl.setContentsMargins(0, 0, 0, 0)
                    row.setLayout(hl)

                    txt = QLineEditX(ch)
                    lbl = QLabel(ch.unit)
                    hl.addWidget(txt)
                    hl.addWidget(lbl)
                    vl.addWidget(row)

                    # save the emitter from text box enter press
                    emitters[chname] = txt.returnPressedX
                
                if ch.mode == 'read' or ch.mode == 'both':
                    # add read channel
                    row2 = QFrame()
                    hl2 = QHBoxLayout()
                    hl2.setContentsMargins(0, 0, 0 ,0)
                    row2.setLayout(hl2)

                    txt2 = QLineEdit()
                    txt2.setDisabled(True)
                    lbl2 = QLabel(ch.unit)
                    hl2.addWidget(txt2)
                    hl2.addWidget(lbl2)
                    vl.addWidget(row2)

                    readboxes[chname] = { 'textbox' : txt2, 'channel' : ch }

                vbox.addWidget(gb)

            elif ch.data_type == bool:
                # need two radio buttons
                hbox = QHBoxLayout()
                gb.setLayout(hbox)
                rbOn = QRadioButtonX('On', ch)
                rbOff = QRadioButtonX('Off', ch)

                if ch.value == 0:
                    rbOff.toggle()
                elif ch.value == 1:
                    rbOn.toggle()
                emitters[chname] = rbOn.toggledX
                hbox.addWidget(rbOn)
                hbox.addWidget(rbOff)

                vbox.addWidget(gb)

        self.update_device_settings()

        return readboxes, emitters
    
    def on_device_error(self, arduino_id, err_msg = 'Error'):
        """ Disable group box if server gives an error """ 
        if self._overview_devices[arduino_id]['groupbox'].isEnabled():
            self._overview_devices[arduino_id]['groupbox'].setEnabled(False)
            lblError = QLabel()
            lblError.setText('<font color="red">' + err_msg.split('ERROR: ')[1] + "</font>")
            self._overview_devices[arduino_id]['layout'].insertWidget(0, lblError)

    def on_device_working(self, arduino_id):
        """ Re-enable group box if server does not give an error """ 
        if not self._overview_devices[arduino_id]['groupbox'].isEnabled():
            self._overview_devices[arduino_id]['groupbox'].setEnabled(True)
            lbl = self._overview_devices[arduino_id]['layout'].takeAt(0)
            lbl.widget().deleteLater()

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

    def update_device_settings(self):
        self.ui.treeDevices.clear()
        self._settings_devices = {}
        for ard_id, data in self._overview_devices.items():
            dev = data['device']
            devrow = QTreeWidgetItem(self.ui.treeDevices)
            devrow.setText(0, dev.label)
            devrow.setText(1, 'Device')
            self._settings_devices[dev.arduino_id] = {'device': dev, 'row': devrow, 'channels': {}}
            for chname, ch in reversed(sorted(dev.channels.items(), key=lambda x: x[1].display_order)):
                chrow = QTreeWidgetItem(devrow)
                chrow.setText(0, ch.label)
                chrow.setText(1, 'Channel')
                self._settings_devices[dev.arduino_id]['channels'][ch.name] = {'channel': ch, 'row': chrow}
            newchrow = QTreeWidgetItem(devrow)
            newchrow.setText(0, '[Add a new Channel]')
            #newchrow.setText(1, 'Channel')

        newdevrow = QTreeWidgetItem(self.ui.treeDevices)
        newdevrow.setText(0, '[Add a new Device]')
        #newdevrow.setText(1, 'Device')

        self.ui.treeDevices.expandAll()

    def on_settings_row_changed(self, item):
        if item == None:
            #self.ui.treeDevices.setCurrentItem(self.ui.treeDevices.topLevelItem(0))
            return

        self.clearLayout(self._devvbox)
        # recover the associated object to change
        obj = None
        parent = None
        for ard_id, data in self._settings_devices.items():
            if data['row'] == item:
                obj = data['device']
                break
            else:
                for name, chdata in data['channels'].items():
                    if item.parent() == data['row']:
                        parent = data['device']
                    if chdata['row'] == item:
                        obj = chdata['channel']
                        break

        if type(obj) == Device or 'device' in item.text(0).lower():
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
            btnSave = QPushButtonObj('Save Changes', obj)
            btnSave.clickedX.connect(self.on_save_changes_click)
            hbox.addWidget(btnSave)
            hbox.addStretch()

            self._devvbox.addLayout(hbox)

            self._devvbox.addStretch()
        elif type(obj) == Channel or 'channel' in item.text(0).lower():
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
                btnSave = QPushButtonObj('Save Changes', 'channel')
            btnSave.clickedX.connect(self.on_save_changes_click)
            hbox.addWidget(btnSave)
            hbox.addStretch()

            self._devvbox.addLayout(hbox)

            self._devvbox.addStretch()

    def on_save_changes_click(self, obj):
        
        #newobj = copy.deepcopy(obj)
        if type(obj) == Device or (type(obj) == str and 'device' in obj.lower()):
            # TODO This is hard-coded to avoid passing references to all the controls around
            # probably not the best solution.

            # locate device in self._overview_devices
            dev = self._overview_devices[obj.arduino_id]['device']

            # make changes
            # order is: name, arduino_id, label -> (1, 3, 5)
            gbox = self._devvbox.itemAt(1).layout()
            dev.name = gbox.itemAt(1).widget().text()
            dev.label = gbox.itemAt(5).widget().text()
            
            new_ard_id = gbox.itemAt(3).widget().text()
            if new_ard_id != dev.arduino_id:
                self._overview_devices[new_ard_id] = self._overview_devices.pop(dev.arduino_id)
                dev.arduino_id = new_ard_id

        elif type(obj) == Channel or (type(obj) == str and 'channel' in obj.lower()):
            ch = obj.parent_device.channels[obj.name]
            gbox = self._devvbox.itemAt(1).layout()

            # order is: name, label, unit, lower, upper, type, mode
            ch.name = gbox.itemAt(1).widget().text()
            ch.label = gbox.itemAt(3).widget().text()
            ch.unit = gbox.itemAt(5).widget().text()

            cbType = gbox.itemAt(11).widget()
            # int, bool, float
            if cbType.currentIndex() == 0:
                ch.data_type = int
            elif cbType.currentIndex() == 1:
                ch.data_type = bool
            else:
                ch.data_type = float

            try:
                ch.lower_limit = ch.data_type(gbox.itemAt(7).widget().text())
                ch.upper_limit = ch.data_type(gbox.itemAt(9).widget().text())
            except:
                print('bad values for limits')
                return

            cbMode = gbox.itemAt(13).widget()
            # read, write, both
            if cbMode.currentIndex() == 0:
                ch.mode = 'read'
            elif cbMode.currentIndex() == 1:
                ch.mode = 'write'
            else:
                ch.mode = 'both'

        self.clearLayout(self._devvbox)
        self.update_device_settings()
        self.sig_device_channel_changed.emit()

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
