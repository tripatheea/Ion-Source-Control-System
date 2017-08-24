# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1163, 629)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.splitter_2.setFont(font)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.frame_3 = QtWidgets.QFrame(self.splitter_2)
        self.frame_3.setMinimumSize(QtCore.QSize(250, 250))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_3.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.frame_3.setFont(font)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.btnStop = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStop.sizePolicy().hasHeightForWidth())
        self.btnStop.setSizePolicy(sizePolicy)
        self.btnStop.setMinimumSize(QtCore.QSize(0, 75))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnStop.setFont(font)
        self.btnStop.setObjectName("btnStop")
        self.gridLayout_3.addWidget(self.btnStop, 0, 0, 1, 1)
        self.splitter_3 = QtWidgets.QSplitter(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.splitter_3.setFont(font)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName("splitter_3")
        self.fmPollRates = QtWidgets.QFrame(self.splitter_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fmPollRates.sizePolicy().hasHeightForWidth())
        self.fmPollRates.setSizePolicy(sizePolicy)
        self.fmPollRates.setMinimumSize(QtCore.QSize(0, 100))
        self.fmPollRates.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fmPollRates.setFont(font)
        self.fmPollRates.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fmPollRates.setFrameShadow(QtWidgets.QFrame.Plain)
        self.fmPollRates.setObjectName("fmPollRates")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.fmPollRates)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lblServPoll = QtWidgets.QLabel(self.fmPollRates)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblServPoll.setFont(font)
        self.lblServPoll.setObjectName("lblServPoll")
        self.verticalLayout_2.addWidget(self.lblServPoll)
        self.label_2 = QtWidgets.QLabel(self.fmPollRates)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gbPinnedPlot = QtWidgets.QGroupBox(self.splitter_3)
        self.gbPinnedPlot.setMinimumSize(QtCore.QSize(0, 250))
        self.gbPinnedPlot.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.gbPinnedPlot.setFont(font)
        self.gbPinnedPlot.setObjectName("gbPinnedPlot")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.gbPinnedPlot)
        self.gridLayout_7.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.pltPinned = PlotWidget(self.gbPinnedPlot)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pltPinned.setFont(font)
        self.pltPinned.setObjectName("pltPinned")
        self.gridLayout_7.addWidget(self.pltPinned, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.splitter_3, 1, 0, 1, 1)
        self.tabMain = QtWidgets.QTabWidget(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabMain.sizePolicy().hasHeightForWidth())
        self.tabMain.setSizePolicy(sizePolicy)
        self.tabMain.setMinimumSize(QtCore.QSize(500, 450))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tabMain.setFont(font)
        self.tabMain.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabMain.setObjectName("tabMain")
        self.overview = QtWidgets.QWidget()
        self.overview.setObjectName("overview")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.overview)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scroller = QtWidgets.QScrollArea(self.overview)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.scroller.setFont(font)
        self.scroller.setAutoFillBackground(False)
        self.scroller.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroller.setWidgetResizable(True)
        self.scroller.setObjectName("scroller")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 546, 491))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.fmOverview = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fmOverview.setFont(font)
        self.fmOverview.setStyleSheet("")
        self.fmOverview.setFrameShape(QtWidgets.QFrame.Box)
        self.fmOverview.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fmOverview.setObjectName("fmOverview")
        self.gridLayout_6.addWidget(self.fmOverview, 0, 0, 1, 1)
        self.scroller.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scroller, 0, 0, 1, 1)
        self.tabMain.addTab(self.overview, "")
        self.devices = QtWidgets.QWidget()
        self.devices.setObjectName("devices")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.devices)
        self.gridLayout_5.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.splitter = QtWidgets.QSplitter(self.devices)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.treeDevices = QtWidgets.QTreeWidget(self.layoutWidget)
        self.treeDevices.setColumnCount(2)
        self.treeDevices.setObjectName("treeDevices")
        self.treeDevices.headerItem().setText(0, "1")
        self.treeDevices.headerItem().setText(1, "2")
        self.treeDevices.header().setDefaultSectionSize(300)
        self.verticalLayout_4.addWidget(self.treeDevices)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnExpand = QtWidgets.QPushButton(self.layoutWidget)
        self.btnExpand.setObjectName("btnExpand")
        self.horizontalLayout.addWidget(self.btnExpand)
        self.btnCollapse = QtWidgets.QPushButton(self.layoutWidget)
        self.btnCollapse.setObjectName("btnCollapse")
        self.horizontalLayout.addWidget(self.btnCollapse)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.fmDeviceSettings = QtWidgets.QFrame(self.splitter)
        self.fmDeviceSettings.setMinimumSize(QtCore.QSize(250, 0))
        self.fmDeviceSettings.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fmDeviceSettings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fmDeviceSettings.setObjectName("fmDeviceSettings")
        self.gridLayout_5.addWidget(self.splitter, 0, 0, 1, 1)
        self.tabMain.addTab(self.devices, "")
        self.plotting = QtWidgets.QWidget()
        self.plotting.setObjectName("plotting")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.plotting)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_4 = QtWidgets.QFrame(self.plotting)
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.frame_4.setFont(font)
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_4.setLineWidth(1)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(7)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnSetupDevicePlots = QtWidgets.QPushButton(self.frame_4)
        self.btnSetupDevicePlots.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnSetupDevicePlots.setFont(font)
        self.btnSetupDevicePlots.setFlat(False)
        self.btnSetupDevicePlots.setObjectName("btnSetupDevicePlots")
        self.horizontalLayout_2.addWidget(self.btnSetupDevicePlots)
        self.verticalLayout_3.addWidget(self.frame_4)
        self.scrollArea = QtWidgets.QScrollArea(self.plotting)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.scrollArea.setFont(font)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 546, 449))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.fmPlots = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fmPlots.setFont(font)
        self.fmPlots.setStyleSheet("")
        self.fmPlots.setFrameShape(QtWidgets.QFrame.Box)
        self.fmPlots.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fmPlots.setObjectName("fmPlots")
        self.gridLayout_4.addWidget(self.fmPlots, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.tabMain.addTab(self.plotting, "")
        self.procedures = QtWidgets.QWidget()
        self.procedures.setObjectName("procedures")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.procedures)
        self.gridLayout_9.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.btnAddProcedure = QtWidgets.QPushButton(self.procedures)
        self.btnAddProcedure.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnAddProcedure.setFont(font)
        self.btnAddProcedure.setFlat(False)
        self.btnAddProcedure.setObjectName("btnAddProcedure")
        self.gridLayout_9.addWidget(self.btnAddProcedure, 0, 0, 1, 1)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.procedures)
        self.scrollArea_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 546, 449))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 11)
        self.gridLayout_10.setSpacing(6)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.fmProcedures = QtWidgets.QFrame(self.scrollAreaWidgetContents_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fmProcedures.setFont(font)
        self.fmProcedures.setStyleSheet("")
        self.fmProcedures.setFrameShape(QtWidgets.QFrame.Box)
        self.fmProcedures.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fmProcedures.setObjectName("fmProcedures")
        self.vboxProcedures = QtWidgets.QVBoxLayout(self.fmProcedures)
        self.vboxProcedures.setContentsMargins(11, 11, 11, 11)
        self.vboxProcedures.setSpacing(6)
        self.vboxProcedures.setObjectName("vboxProcedures")
        self.gridLayout_10.addWidget(self.fmProcedures, 0, 0, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout_9.addWidget(self.scrollArea_2, 1, 0, 1, 1)
        self.tabMain.addTab(self.procedures, "")
        self.log = QtWidgets.QWidget()
        self.log.setObjectName("log")
        self.gridLayout = QtWidgets.QGridLayout(self.log)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.txtMessageLog = QtWidgets.QTextEdit(self.log)
        self.txtMessageLog.setFrameShape(QtWidgets.QFrame.Box)
        self.txtMessageLog.setReadOnly(True)
        self.txtMessageLog.setObjectName("txtMessageLog")
        self.gridLayout.addWidget(self.txtMessageLog, 0, 0, 1, 1)
        self.tabMain.addTab(self.log, "")
        self.verticalLayout.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.toolBar.setFont(font)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.btnQuit = QtWidgets.QAction(MainWindow)
        self.btnQuit.setObjectName("btnQuit")
        self.btnLoad = QtWidgets.QAction(MainWindow)
        self.btnLoad.setObjectName("btnLoad")
        self.btnSave = QtWidgets.QAction(MainWindow)
        self.btnSave.setObjectName("btnSave")
        self.toolBar.addAction(self.btnQuit)
        self.toolBar.addAction(self.btnLoad)
        self.toolBar.addAction(self.btnSave)

        self.retranslateUi(MainWindow)
        self.tabMain.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ion Source Control System"))
        self.btnStop.setText(_translate("MainWindow", "Emergency Stop"))
        self.lblServPoll.setText(_translate("MainWindow", "Server Polling Rate: 15 Hz"))
        self.label_2.setText(_translate("MainWindow", "Device 1 Polling Rate: 15 Hz"))
        self.gbPinnedPlot.setTitle(_translate("MainWindow", "Pinned Plot"))
        self.tabMain.setTabText(self.tabMain.indexOf(self.overview), _translate("MainWindow", "Overview"))
        self.treeDevices.setSortingEnabled(True)
        self.btnExpand.setText(_translate("MainWindow", "Expand All"))
        self.btnCollapse.setText(_translate("MainWindow", "Collapse All"))
        self.tabMain.setTabText(self.tabMain.indexOf(self.devices), _translate("MainWindow", "Devices"))
        self.btnSetupDevicePlots.setText(_translate("MainWindow", "Choose Channels to Plot"))
        self.tabMain.setTabText(self.tabMain.indexOf(self.plotting), _translate("MainWindow", "Plotting"))
        self.btnAddProcedure.setText(_translate("MainWindow", "Add Procedure"))
        self.tabMain.setTabText(self.tabMain.indexOf(self.procedures), _translate("MainWindow", "Procedures"))
        self.tabMain.setTabText(self.tabMain.indexOf(self.log), _translate("MainWindow", "Message Log"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.btnQuit.setText(_translate("MainWindow", "Quit"))
        self.btnLoad.setText(_translate("MainWindow", "Load Devices"))
        self.btnLoad.setToolTip(_translate("MainWindow", "Load Devices"))
        self.btnSave.setText(_translate("MainWindow", "Save Devices"))

from pyqtgraph import PlotWidget
