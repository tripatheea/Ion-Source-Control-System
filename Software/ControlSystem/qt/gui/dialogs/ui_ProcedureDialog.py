# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ProcedureDialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProcedureDialog(object):
    def setupUi(self, ProcedureDialog):
        ProcedureDialog.setObjectName("ProcedureDialog")
        ProcedureDialog.resize(1106, 876)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        ProcedureDialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProcedureDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.label = QtWidgets.QLabel(ProcedureDialog)
        self.label.setObjectName("label")
        self.horizontalLayout_7.addWidget(self.label)
        self.txtProcedureName = QtWidgets.QLineEdit(ProcedureDialog)
        self.txtProcedureName.setAlignment(QtCore.Qt.AlignCenter)
        self.txtProcedureName.setObjectName("txtProcedureName")
        self.horizontalLayout_7.addWidget(self.txtProcedureName)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.tabWidget = QtWidgets.QTabWidget(ProcedureDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.rbValue = QtWidgets.QRadioButton(self.groupBox_2)
        self.rbValue.setChecked(True)
        self.rbValue.setObjectName("rbValue")
        self.gridLayout_3.addWidget(self.rbValue, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.cbRuleDevice = QtWidgets.QComboBox(self.groupBox_2)
        self.cbRuleDevice.setCurrentText("")
        self.cbRuleDevice.setObjectName("cbRuleDevice")
        self.horizontalLayout_3.addWidget(self.cbRuleDevice)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.cbRuleChannel = QtWidgets.QComboBox(self.groupBox_2)
        self.cbRuleChannel.setCurrentText("")
        self.cbRuleChannel.setObjectName("cbRuleChannel")
        self.horizontalLayout_3.addWidget(self.cbRuleChannel)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.cbRuleCompare = QtWidgets.QComboBox(self.groupBox_2)
        self.cbRuleCompare.setCurrentText("")
        self.cbRuleCompare.setObjectName("cbRuleCompare")
        self.horizontalLayout_3.addWidget(self.cbRuleCompare)
        self.cbRuleBool = QtWidgets.QComboBox(self.groupBox_2)
        self.cbRuleBool.setObjectName("cbRuleBool")
        self.horizontalLayout_3.addWidget(self.cbRuleBool)
        self.txtRuleVal = QtWidgets.QLineEdit(self.groupBox_2)
        self.txtRuleVal.setAlignment(QtCore.Qt.AlignCenter)
        self.txtRuleVal.setObjectName("txtRuleVal")
        self.horizontalLayout_3.addWidget(self.txtRuleVal)
        self.lblRuleUnit = QtWidgets.QLabel(self.groupBox_2)
        self.lblRuleUnit.setObjectName("lblRuleUnit")
        self.horizontalLayout_3.addWidget(self.lblRuleUnit)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)
        self.rbEvent = QtWidgets.QRadioButton(self.groupBox_2)
        self.rbEvent.setObjectName("rbEvent")
        self.gridLayout_3.addWidget(self.rbEvent, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.cbEvent = QtWidgets.QComboBox(self.groupBox_2)
        self.cbEvent.setEnabled(False)
        self.cbEvent.setObjectName("cbEvent")
        self.horizontalLayout_5.addWidget(self.cbEvent)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)
        self.rbManual = QtWidgets.QRadioButton(self.groupBox_2)
        self.rbManual.setObjectName("rbManual")
        self.gridLayout_3.addWidget(self.rbManual, 2, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 475))
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_8.addWidget(self.label_2)
        self.cbActionDevice = QtWidgets.QComboBox(self.groupBox_3)
        self.cbActionDevice.setCurrentText("")
        self.cbActionDevice.setObjectName("cbActionDevice")
        self.horizontalLayout_8.addWidget(self.cbActionDevice)
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_8.addWidget(self.label_5)
        self.cbActionChannel = QtWidgets.QComboBox(self.groupBox_3)
        self.cbActionChannel.setCurrentText("")
        self.cbActionChannel.setObjectName("cbActionChannel")
        self.horizontalLayout_8.addWidget(self.cbActionChannel)
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.cbActionBool = QtWidgets.QComboBox(self.groupBox_3)
        self.cbActionBool.setObjectName("cbActionBool")
        self.horizontalLayout_8.addWidget(self.cbActionBool)
        self.txtActionVal = QtWidgets.QLineEdit(self.groupBox_3)
        self.txtActionVal.setAlignment(QtCore.Qt.AlignCenter)
        self.txtActionVal.setObjectName("txtActionVal")
        self.horizontalLayout_8.addWidget(self.txtActionVal)
        self.lblActionUnit = QtWidgets.QLabel(self.groupBox_3)
        self.lblActionUnit.setObjectName("lblActionUnit")
        self.horizontalLayout_8.addWidget(self.lblActionUnit)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem6)
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit.setMaxLength(10)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_8.addWidget(self.lineEdit)
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem7)
        self.btnAddAction = QtWidgets.QPushButton(self.groupBox_3)
        self.btnAddAction.setObjectName("btnAddAction")
        self.horizontalLayout_8.addWidget(self.btnAddAction)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.scAction = QtWidgets.QScrollArea(self.groupBox_3)
        self.scAction.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scAction.setWidgetResizable(True)
        self.scAction.setObjectName("scAction")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1032, 242))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.fmActions = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.fmActions.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fmActions.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fmActions.setObjectName("fmActions")
        self.gridLayout.addWidget(self.fmActions, 0, 0, 1, 1)
        self.scAction.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scAction)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem8 = QtWidgets.QSpacerItem(256, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem8)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem9)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem10)
        self.cbPidDevice = QtWidgets.QComboBox(self.tab_2)
        self.cbPidDevice.setCurrentText("")
        self.cbPidDevice.setObjectName("cbPidDevice")
        self.horizontalLayout_4.addWidget(self.cbPidDevice)
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_4.addWidget(self.label_9)
        self.cbPidChannel = QtWidgets.QComboBox(self.tab_2)
        self.cbPidChannel.setCurrentText("")
        self.cbPidChannel.setObjectName("cbPidChannel")
        self.horizontalLayout_4.addWidget(self.cbPidChannel)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem11)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_10.addWidget(self.label_10)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_10.addWidget(self.lineEdit_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_11 = QtWidgets.QLabel(self.groupBox_5)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 0, 0, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_4.addWidget(self.lineEdit_6, 0, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox_5)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 1, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_4.addWidget(self.lineEdit_3, 1, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox_5)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_4.addWidget(self.lineEdit_4, 2, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox_5)
        self.label_14.setObjectName("label_14")
        self.gridLayout_4.addWidget(self.label_14, 3, 0, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_4.addWidget(self.lineEdit_5, 3, 1, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_6)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_11.addWidget(self.checkBox)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.horizontalLayout_11.addWidget(self.lineEdit_7)
        self.label_15 = QtWidgets.QLabel(self.groupBox_6)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_11.addWidget(self.label_15)
        self.verticalLayout_4.addWidget(self.groupBox_6)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem12)
        self.horizontalLayout_12.addLayout(self.verticalLayout_4)
        spacerItem13 = QtWidgets.QSpacerItem(256, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem13)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.groupBox = QtWidgets.QGroupBox(ProcedureDialog)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chkCritical = QtWidgets.QCheckBox(self.groupBox)
        self.chkCritical.setObjectName("chkCritical")
        self.horizontalLayout.addWidget(self.chkCritical)
        self.horizontalLayout_9.addWidget(self.groupBox)
        self.groupBox_4 = QtWidgets.QGroupBox(ProcedureDialog)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.chkEmail = QtWidgets.QCheckBox(self.groupBox_4)
        self.chkEmail.setObjectName("chkEmail")
        self.horizontalLayout_6.addWidget(self.chkEmail)
        self.chkText = QtWidgets.QCheckBox(self.groupBox_4)
        self.chkText.setObjectName("chkText")
        self.horizontalLayout_6.addWidget(self.chkText)
        self.horizontalLayout_9.addWidget(self.groupBox_4)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.gbContact = QtWidgets.QGroupBox(ProcedureDialog)
        self.gbContact.setObjectName("gbContact")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gbContact)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lblEmail = QtWidgets.QLabel(self.gbContact)
        self.lblEmail.setObjectName("lblEmail")
        self.gridLayout_2.addWidget(self.lblEmail, 0, 1, 1, 1)
        self.lblText = QtWidgets.QLabel(self.gbContact)
        self.lblText.setObjectName("lblText")
        self.gridLayout_2.addWidget(self.lblText, 1, 1, 1, 1)
        self.txtText = QtWidgets.QLineEdit(self.gbContact)
        self.txtText.setObjectName("txtText")
        self.gridLayout_2.addWidget(self.txtText, 1, 2, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem14, 0, 3, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem15, 1, 0, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem16, 0, 0, 1, 1)
        self.txtEmail = QtWidgets.QLineEdit(self.gbContact)
        self.txtEmail.setObjectName("txtEmail")
        self.gridLayout_2.addWidget(self.txtEmail, 0, 2, 1, 1)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem17, 1, 3, 1, 1)
        self.verticalLayout.addWidget(self.gbContact)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem18)
        self.btnDone = QtWidgets.QPushButton(ProcedureDialog)
        self.btnDone.setObjectName("btnDone")
        self.horizontalLayout_2.addWidget(self.btnDone)
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem19)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ProcedureDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ProcedureDialog)

    def retranslateUi(self, ProcedureDialog):
        _translate = QtCore.QCoreApplication.translate
        ProcedureDialog.setWindowTitle(_translate("ProcedureDialog", "Add/Edit Procedure"))
        self.label.setText(_translate("ProcedureDialog", "Name"))
        self.txtProcedureName.setText(_translate("ProcedureDialog", "My Procedure"))
        self.groupBox_2.setTitle(_translate("ProcedureDialog", "Rule"))
        self.rbValue.setText(_translate("ProcedureDialog", "Value"))
        self.label_3.setText(_translate("ProcedureDialog", "."))
        self.label_4.setText(_translate("ProcedureDialog", "is"))
        self.lblRuleUnit.setText(_translate("ProcedureDialog", "TextLabel"))
        self.rbEvent.setText(_translate("ProcedureDialog", "Event"))
        self.rbManual.setText(_translate("ProcedureDialog", "Manual"))
        self.groupBox_3.setTitle(_translate("ProcedureDialog", "Action"))
        self.label_2.setText(_translate("ProcedureDialog", "Set"))
        self.label_5.setText(_translate("ProcedureDialog", "."))
        self.label_6.setText(_translate("ProcedureDialog", "to"))
        self.lblActionUnit.setText(_translate("ProcedureDialog", "TextLabel"))
        self.label_7.setText(_translate("ProcedureDialog", "Delay:"))
        self.lineEdit.setText(_translate("ProcedureDialog", "0.0"))
        self.label_8.setText(_translate("ProcedureDialog", "s"))
        self.btnAddAction.setText(_translate("ProcedureDialog", "Add"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("ProcedureDialog", "Basic"))
        self.label_9.setText(_translate("ProcedureDialog", "."))
        self.label_10.setText(_translate("ProcedureDialog", "Target Value:"))
        self.lineEdit_2.setText(_translate("ProcedureDialog", "0.0"))
        self.groupBox_5.setTitle(_translate("ProcedureDialog", "PID"))
        self.label_11.setText(_translate("ProcedureDialog", "Time Step:"))
        self.lineEdit_6.setText(_translate("ProcedureDialog", "0.0"))
        self.label_12.setText(_translate("ProcedureDialog", "P"))
        self.lineEdit_3.setText(_translate("ProcedureDialog", "0.0"))
        self.label_13.setText(_translate("ProcedureDialog", "I"))
        self.lineEdit_4.setText(_translate("ProcedureDialog", "0.0"))
        self.label_14.setText(_translate("ProcedureDialog", "D"))
        self.lineEdit_5.setText(_translate("ProcedureDialog", "0.0"))
        self.groupBox_6.setTitle(_translate("ProcedureDialog", "Options"))
        self.checkBox.setText(_translate("ProcedureDialog", "Stop when value is within"))
        self.lineEdit_7.setText(_translate("ProcedureDialog", "0.0"))
        self.label_15.setText(_translate("ProcedureDialog", "% of target"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("ProcedureDialog", "PID"))
        self.groupBox.setTitle(_translate("ProcedureDialog", "Options"))
        self.chkCritical.setText(_translate("ProcedureDialog", "Critical"))
        self.groupBox_4.setTitle(_translate("ProcedureDialog", "Notify"))
        self.chkEmail.setText(_translate("ProcedureDialog", "Email"))
        self.chkText.setText(_translate("ProcedureDialog", "Text"))
        self.gbContact.setTitle(_translate("ProcedureDialog", "Contact Information"))
        self.lblEmail.setText(_translate("ProcedureDialog", "Email"))
        self.lblText.setText(_translate("ProcedureDialog", "Mobile"))
        self.btnDone.setText(_translate("ProcedureDialog", "Done"))

