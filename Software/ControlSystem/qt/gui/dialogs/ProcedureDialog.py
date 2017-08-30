#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Thomas Wester <twester@mit.edu>
# Dialog for creating/editing procedures

import operator

from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QPushButton, QVBoxLayout, \
                            QHBoxLayout
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from .ui_ProcedureDialog import Ui_ProcedureDialog
from lib.Procedure import Procedure

class ProcedureDialog(QDialog):

    def __init__(self, devices, procnames, proc=None):
        super().__init__()
        self.ui = Ui_ProcedureDialog()
        self.ui.setupUi(self)

        self._devdict = devices

        # maintain order of the list of devices
        self._devlist = [x for name, x in self._devdict.items()]
        self._actions = {}
        self._actioncontrols = {}
        self._procnames = procnames # need this to check that we don't add two procedures of the same name

        # if proc = None, assume this is for a new procedure
        # else, we are editing a procedure

        self._newproc = proc
        self._accepted = False

        self.initialize()

    def initialize(self):
        # set up UI elements
        self.ui.cbActionBool.addItems(['On', 'Off'])
        self.ui.cbActionBool.hide()
        self.ui.cbRuleBool.addItems(['On', 'Off'])
        self.ui.cbRuleBool.hide()
        self.ui.lblRuleUnit.hide()
        self.ui.lblActionUnit.hide()
        self.ui.lblEmail.hide()
        self.ui.txtEmail.hide()
        self.ui.lblText.hide()
        self.ui.txtText.hide()
        self.ui.gbContact.hide()

        self.ui.btnDone.clicked.connect(self.on_done_click)
        self.ui.cbRuleDevice.currentIndexChanged.connect(self.on_rule_device_cb_changed)
        self.ui.cbRuleChannel.currentIndexChanged.connect(self.on_rule_channel_cb_changed)
        self.ui.cbActionDevice.currentIndexChanged.connect(self.on_action_device_cb_changed)
        self.ui.cbActionChannel.currentIndexChanged.connect(self.on_action_channel_cb_changed)
        self.ui.btnAddAction.clicked.connect(self.on_add_action_click)
        self.ui.chkEmail.stateChanged.connect(self.on_email_check_changed)
        self.ui.chkText.stateChanged.connect(self.on_text_check_changed)

        self._vboxActions = QVBoxLayout()
        self._vboxActions.addStretch()
        self.ui.fmActions.setLayout(self._vboxActions)

        # Fill comboboxes with devices/channels
        devnamelist = [x.label for x in self._devlist]
        self.ui.cbRuleDevice.addItems([' - Choose a device - '] + devnamelist)
        self.ui.cbActionDevice.addItems([' - Choose a device - '] + devnamelist)
        self.ui.cbRuleCompare.addItems(['<', '>', '=', '<=', '>='])

        if self._newproc != None:
            # we are editing a procedure, so fill in the procedure info
            self.ui.txtProcedureName.setText(self._newproc.name)

            for idx, rule in self._newproc.rules.items():
                # TODO: currently only works with 1 rule
                for i, dev in enumerate(self._devlist):
                    if rule['device'] == dev:
                        # Set device combobox
                        self.ui.cbRuleDevice.setCurrentIndex(i + 1)
                        break

                chs = rule['device'].channels
                chlist = [x for name, x in reversed(sorted(chs.items(), key=lambda t: t[1].display_order))]
                for i, ch in enumerate(chlist):
                    # Set channel combobox
                    if rule['channel'] == ch:
                        self.ui.cbRuleChannel.setCurrentIndex(i + 1)
                        break
                
                # Set comparison operator and value
                if rule['channel'].data_type != bool:
                    self.ui.txtRuleVal.setText(str(rule['value']))
                    if rule['comp'] == operator.lt:
                        self.ui.cbRuleCompare.setCurrentIndex(0)
                    if rule['comp'] == operator.gt:
                        self.ui.cbRuleCompare.setCurrentIndex(1)
                    if rule['comp'] == operator.eq:
                        self.ui.cbRuleCompare.setCurrentIndex(2)
                    if rule['comp'] == operator.le:
                        self.ui.cbRuleCompare.setCurrentIndex(3)
                    if rule['comp'] == operator.ge:
                        self.ui.cbRuleCompare.setCurrentIndex(4)

                else:
                    # since we already changed the index to a channel of type bool,
                    # the bool combo box should be visible
                    if rule['value']:
                        self.ui.cbRuleBool.setCurrentIndex(0)
                    else:
                        self.ui.cbRuleBool.setCurrentIndex(1)

            # add the actions
            for idx, action in self._newproc.actions.items():
                for i, dev in enumerate(self._devlist):
                    #set the device combobox
                    if action['device'] == dev:
                        self.ui.cbActionDevice.setCurrentIndex(i + 1)
                        break

                chs = action['device'].channels
                chlist = [x for name, x in reversed(sorted(chs.items(), key=lambda t: t[1].display_order))]
                for i, ch in enumerate(chlist):
                    # Set channel combobox
                    if action['channel'] == ch:
                        self.ui.cbActionChannel.setCurrentIndex(i + 1)
                        break

                # set the data text
                if action['channel'].data_type != bool:
                    self.ui.txtActionVal.setText(str(action['value']))
                else:
                    if action['value']:
                        self.ui.cbActionBool.setCurrentIndex(0)
                    else:
                        self.ui.cbActionBool.setCurrentIndex(1)

                self.on_add_action_click()



            if self._newproc.critical:
                self.ui.chkCritical.toggle()

            if self._newproc.email != '':
                self.ui.chkEmail.toggle()
                self.ui.gbContact.show()
                self.ui.lblEmail.show()
                self.ui.txtEmail.show()
                self.ui.txtEmail.setText(self._newproc.email)

            if self._newproc.sms != '':
                self.ui.chkText.toggle()
                self.ui.gbContact.show()
                self.ui.lblText.show()
                self.ui.txtText.show()
                self.ui.txtText.setText(self._newproc.sms)


    def on_add_action_click(self):
        if self.ui.cbActionDevice.currentIndex() == 0 or self.ui.cbActionChannel.currentIndex() == 0:
            return

        device = self._devlist[self.ui.cbActionDevice.currentIndex() - 1]
        chs = device.channels
        chlist = [x for name, x in reversed(sorted(chs.items(), key=lambda t: t[1].display_order))]
        channel = chlist[self.ui.cbActionChannel.currentIndex() - 1]
        if channel.data_type != bool:
            try:
                value = channel.data_type(self.ui.txtActionVal.text())
            except:
                print('Error: Bad input')
                return

            if value > channel.upper_limit or value < channel.lower_limit:
                print('Error: Exceeded channel limits')
                return
        else:
            if self.ui.cbActionBool.currentText() == 'On':
                value = True
            else:
                value = False
            
        index = len(self._actions)

        fm = QFrame()
        
        vbox = QVBoxLayout()
        lblDevCh = QLabel(self.ui.cbActionDevice.currentText() + '.' + \
                          self.ui.cbActionChannel.currentText())
        if channel.data_type != bool:
            lblSetVal = QLabel('Set value: {} {}'.format(str(value), channel.unit))
        else:
            if value:
                lblSetVal = QLabel('Set value: On')
            else:
                lblSetVal = QLabel('Set value: Off')

        vbox.addWidget(lblDevCh)
        vbox.addWidget(lblSetVal)

        btnDel = QPushButtonX('Delete', index)
        btnDel.clickedX.connect(self.on_delete_action_click)

        hbox = QHBoxLayout()
        lblNum = QLabel(str(index + 1) + ') ')
        hbox.addWidget(lblNum)
        hbox.addLayout(vbox)
        hbox.addStretch()
        hbox.addWidget(btnDel)

        fm.setLayout(hbox)

        self._vboxActions.insertWidget(0, fm)

        self.ui.txtActionVal.setText('')
        self.ui.cbActionDevice.setCurrentIndex(0)
        self.ui.cbActionBool.hide()
        self.ui.txtActionVal.show()

        self._actions[index] = {'device' : device, 'channel' : channel, 'value' : value}
        self._actioncontrols[index] = {'button' : btnDel, 'frame' : fm, 'label' : lblNum, 'layout' : hbox}

    def on_delete_action_click(self, index):
        del self._actions[index]
        self._actioncontrols[index]['frame'].deleteLater()
        del self._actioncontrols[index]

        # fix numbering of actions. Shift all actions above the deleted one by 1
        # e.g. in list of 0,1,2,3 -> Delete 1 -> shift 2 to 1, 3 to 2
        newactions = {}
        newactioncontrols = {}
        
        actionlist = [action for idx, action in sorted(self._actions.items(), key=lambda t: int(t[0]))]
        actioncontrollist = [controls for idx, controls in sorted(self._actioncontrols.items(), key=lambda t: int(t[0]))]
        
        # get rid of the pesky old-indexed buttons
        for control in actioncontrollist:
            control['button'].deleteLater()
            del control['button']

        for i, action in enumerate(actionlist):
            # fill shifted lists
            newactions[i] = action
            
            controls = actioncontrollist[i]
            controls['label'].setText(str(i + 1) + ') ')
            btnDel = QPushButtonX('Delete', i)
            btnDel.clickedX.connect(self.on_delete_action_click)
            controls['button'] = btnDel
            controls['layout'].addWidget(btnDel)

            newactioncontrols[i] = controls

        self._actions = newactions
        self._actioncontrols = newactioncontrols

    def on_rule_device_cb_changed(self, index):
        if index > 0:
            self.ui.cbRuleChannel.clear()
            chs = self._devlist[index - 1].channels
            chlist = [x.label for name, x in reversed(sorted(chs.items(), key=lambda t: t[1].display_order))]
            self.ui.cbRuleChannel.addItems(['- Choose a channel -'] + chlist)
        else:
            self.ui.cbRuleChannel.clear()
            self.ui.cbRuleChannel.addItems(['- Choose a device - '])

    def on_rule_channel_cb_changed(self, index):
        if index > 0:
            chs = self._devlist[self.ui.cbRuleDevice.currentIndex() - 1].channels
            chlist = [x for name, x in reversed(sorted(chs.items(), key=lambda t: t[1].display_order))]
            currentChannel = chlist[index - 1]
            self.ui.lblRuleUnit.setText(currentChannel.unit)
            if currentChannel.data_type == bool:
                # switch text field for combobox
                self.ui.cbRuleBool.show()
                self.ui.txtRuleVal.hide()
                self.ui.lblRuleUnit.hide()
                self.ui.cbRuleCompare.hide()
            else:
                # switch combobox for test field
                self.ui.cbRuleBool.hide()
                self.ui.txtRuleVal.show()
                self.ui.lblRuleUnit.show()
                self.ui.cbRuleCompare.show()
        else:
            self.ui.cbRuleBool.hide()
            self.ui.txtRuleVal.show()
            self.ui.cbRuleCompare.show()


    def on_action_device_cb_changed(self, index):
        if index > 0:
            self.ui.cbActionChannel.clear()
            chs = self._devlist[index - 1].channels
            chlist = [x.label for name, x in reversed(sorted(chs.items(), key=lambda t: t[1].display_order))]
            self.ui.cbActionChannel.addItems(['- Choose a channel -'] + chlist)
        else:
            self.ui.cbActionChannel.clear()
            self.ui.cbActionChannel.addItems(['- Choose a device - '])

    def on_action_channel_cb_changed(self, index):
        if index > 0:
            chs = self._devlist[self.ui.cbActionDevice.currentIndex() - 1].channels
            chlist = [x for name, x in reversed(sorted(chs.items(), key=lambda t: t[1].display_order))]
            currentChannel = chlist[index - 1]
            self.ui.lblActionUnit.setText(currentChannel.unit)
            if currentChannel.data_type == bool:
                # switch text field for combobox
                self.ui.cbActionBool.show()
                self.ui.lblActionUnit.hide()
                self.ui.txtActionVal.hide()
            else:
                # switch combobox for test field
                self.ui.cbActionBool.hide()
                self.ui.lblActionUnit.show()
                self.ui.txtActionVal.show()
        else:
            # switch combobox for test field
            self.ui.cbActionBool.hide()
            self.ui.txtActionVal.show()

    def on_email_check_changed(self, isChecked):
        if isChecked:
            self.ui.gbContact.show()
            self.ui.txtEmail.show()
            self.ui.lblEmail.show()
        else:
            self.ui.txtEmail.hide()
            self.ui.lblEmail.hide()
            self.ui.txtEmail.setText('')
            if not self.ui.chkText.isChecked():
                self.ui.gbContact.hide()

    def on_text_check_changed(self, isChecked):
        if isChecked:
            self.ui.gbContact.show()
            self.ui.txtText.show()
            self.ui.lblText.show()
        else:
            self.ui.txtText.hide()
            self.ui.lblText.hide()
            self.ui.txtText.setText('')
            if not self.ui.chkEmail.isChecked():
                self.ui.gbContact.hide()

    def validate_form(self):
        if self._newproc == None and self.ui.txtProcedureName.text() in self._procnames:
            # if self._newproc is not None, then we are editing a procedure, so ok to overwrite
            print('Error: Procedure name already in use')
            return False

        ruledevidx = self.ui.cbRuleDevice.currentIndex() - 1
        rulechidx = self.ui.cbRuleChannel.currentIndex() - 1
        
        if ruledevidx < 0 or rulechidx < 0:
            # Device or channel not selected for rule
            print('Error: Device or channel not selected for Procedure rule')
            return False

        device = self._devlist[ruledevidx]
        chs = device.channels
        chlist = [x for name, x in reversed(sorted(chs.items(), key=lambda t: t[1].display_order))]
        currentChannel = chlist[rulechidx]

        if currentChannel.data_type != bool:
            try:
                value = currentChannel.data_type(self.ui.txtRuleVal.text())
            except:
                print('Error: Bad value for Rule')
                return False
        else:
            if self.ui.cbRuleBool.currentText() == 'On':
                value = True
            else:
                value = False

        if currentChannel.data_type != bool:
            comptext = self.ui.cbRuleCompare.currentText()
            if comptext == '=':
                comp = operator.eq
            elif comptext == '>':
                comp = operator.gt
            elif comptext == '<':
                comp = operator.lt
            elif comptext == '>=':
                comp = operator.ge
            elif comptext == '<=':
                comp = operator.le
        else:
            comp = operator.eq


        rule = {'1' : {'device' : device, 'channel' : currentChannel, 'value' : value,
                        'comp' : comp}}

        self._newproc = Procedure(self.ui.txtProcedureName.text(), 
                                  rule, self._actions, 
                                  self.ui.chkCritical.isChecked(), 
                                  self.ui.txtEmail.text(), 
                                  self.ui.txtText.text())

        print('Created new procedure:')
        print(self._newproc)

        return True


    def on_done_click(self):
        if self.validate_form():
            self._accepted = True
            self.accept()

    def exec_(self):
        super(ProcedureDialog, self).exec_()
        return self._accepted, self._newproc

class QPushButtonX(QPushButton):
    """ QPushButton which returns its index """
    clickedX = pyqtSignal(int)

    def __init__(self, text, index):
        super().__init__()
        self._index = index
        self.setText(text)
        self.clicked.connect(self.on_clicked)

    @pyqtSlot()
    def on_clicked(self):
        self.clickedX.emit(self._index)