# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/ui_mass_density.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(462, 502)
        MainWindow.setDocumentMode(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.mass_density_radio_button = QtGui.QRadioButton(self.centralwidget)
        self.mass_density_radio_button.setChecked(True)
        self.mass_density_radio_button.setObjectName(_fromUtf8("mass_density_radio_button"))
        self.horizontalLayout_6.addWidget(self.mass_density_radio_button)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.mass_density_line_edit = QtGui.QLineEdit(self.frame)
        self.mass_density_line_edit.setObjectName(_fromUtf8("mass_density_line_edit"))
        self.horizontalLayout_3.addWidget(self.mass_density_line_edit)
        self.mass_density_label = QtGui.QLabel(self.frame)
        self.mass_density_label.setObjectName(_fromUtf8("mass_density_label"))
        self.horizontalLayout_3.addWidget(self.mass_density_label)
        spacerItem = QtGui.QSpacerItem(112, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_6.addWidget(self.frame)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.mass_density_error_message = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mass_density_error_message.sizePolicy().hasHeightForWidth())
        self.mass_density_error_message.setSizePolicy(sizePolicy)
        self.mass_density_error_message.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.mass_density_error_message.setObjectName(_fromUtf8("mass_density_error_message"))
        self.horizontalLayout_9.addWidget(self.mass_density_error_message)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setMinimumSize(QtCore.QSize(30, 30))
        self.label_7.setMaximumSize(QtCore.QSize(30, 30))
        self.label_7.setText(_fromUtf8(""))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_9.addWidget(self.label_7)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        spacerItem1 = QtGui.QSpacerItem(441, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.number_density_radio_button = QtGui.QRadioButton(self.centralwidget)
        self.number_density_radio_button.setObjectName(_fromUtf8("number_density_radio_button"))
        self.horizontalLayout_7.addWidget(self.number_density_radio_button)
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.number_density_line_edit = QtGui.QLineEdit(self.frame_2)
        self.number_density_line_edit.setObjectName(_fromUtf8("number_density_line_edit"))
        self.horizontalLayout_4.addWidget(self.number_density_line_edit)
        self.number_density_units = QtGui.QLabel(self.frame_2)
        self.number_density_units.setObjectName(_fromUtf8("number_density_units"))
        self.horizontalLayout_4.addWidget(self.number_density_units)
        spacerItem2 = QtGui.QSpacerItem(69, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.horizontalLayout_7.addWidget(self.frame_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.number_density_error_message = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.number_density_error_message.sizePolicy().hasHeightForWidth())
        self.number_density_error_message.setSizePolicy(sizePolicy)
        self.number_density_error_message.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.number_density_error_message.setObjectName(_fromUtf8("number_density_error_message"))
        self.horizontalLayout_10.addWidget(self.number_density_error_message)
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setMinimumSize(QtCore.QSize(30, 30))
        self.label_10.setMaximumSize(QtCore.QSize(30, 30))
        self.label_10.setText(_fromUtf8(""))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_10.addWidget(self.label_10)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        spacerItem3 = QtGui.QSpacerItem(441, 26, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.mass_geometry_radio_button = QtGui.QRadioButton(self.centralwidget)
        self.mass_geometry_radio_button.setText(_fromUtf8(""))
        self.mass_geometry_radio_button.setObjectName(_fromUtf8("mass_geometry_radio_button"))
        self.horizontalLayout_8.addWidget(self.mass_geometry_radio_button)
        self.frame_3 = QtGui.QFrame(self.centralwidget)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(self.frame_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.mass_line_edit = QtGui.QLineEdit(self.frame_3)
        self.mass_line_edit.setObjectName(_fromUtf8("mass_line_edit"))
        self.horizontalLayout.addWidget(self.mass_line_edit)
        self.label_4 = QtGui.QLabel(self.frame_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_5 = QtGui.QLabel(self.frame_3)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.geometry_label = QtGui.QLabel(self.frame_3)
        self.geometry_label.setObjectName(_fromUtf8("geometry_label"))
        self.horizontalLayout_2.addWidget(self.geometry_label)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.label = QtGui.QLabel(self.frame_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_11.addWidget(self.label)
        self.volume_label = QtGui.QLabel(self.frame_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volume_label.sizePolicy().hasHeightForWidth())
        self.volume_label.setSizePolicy(sizePolicy)
        self.volume_label.setMinimumSize(QtCore.QSize(100, 0))
        self.volume_label.setObjectName(_fromUtf8("volume_label"))
        self.horizontalLayout_11.addWidget(self.volume_label)
        self.volume_units = QtGui.QLabel(self.frame_3)
        self.volume_units.setObjectName(_fromUtf8("volume_units"))
        self.horizontalLayout_11.addWidget(self.volume_units)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.horizontalLayout_8.addWidget(self.frame_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.mass_error_message = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mass_error_message.sizePolicy().hasHeightForWidth())
        self.mass_error_message.setSizePolicy(sizePolicy)
        self.mass_error_message.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.mass_error_message.setObjectName(_fromUtf8("mass_error_message"))
        self.verticalLayout_2.addWidget(self.mass_error_message)
        spacerItem7 = QtGui.QSpacerItem(441, 17, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem7)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.cancel = QtGui.QPushButton(self.centralwidget)
        self.cancel.setObjectName(_fromUtf8("cancel"))
        self.horizontalLayout_12.addWidget(self.cancel)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem8)
        self.ok = QtGui.QPushButton(self.centralwidget)
        self.ok.setObjectName(_fromUtf8("ok"))
        self.horizontalLayout_12.addWidget(self.ok)
        self.verticalLayout_2.addLayout(self.horizontalLayout_12)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 462, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.ok, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.accept)
        QtCore.QObject.connect(self.number_density_radio_button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.radio_button_changed)
        QtCore.QObject.connect(self.number_density_line_edit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), MainWindow.number_density_value_changed)
        QtCore.QObject.connect(self.mass_line_edit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), MainWindow.mass_value_changed)
        QtCore.QObject.connect(self.mass_geometry_radio_button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.radio_button_changed)
        QtCore.QObject.connect(self.mass_density_radio_button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.radio_button_changed)
        QtCore.QObject.connect(self.mass_density_line_edit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), MainWindow.mass_density_value_changed)
        QtCore.QObject.connect(self.cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.mass_density_radio_button, self.number_density_radio_button)
        MainWindow.setTabOrder(self.number_density_radio_button, self.mass_geometry_radio_button)
        MainWindow.setTabOrder(self.mass_geometry_radio_button, self.mass_density_line_edit)
        MainWindow.setTabOrder(self.mass_density_line_edit, self.number_density_line_edit)
        MainWindow.setTabOrder(self.number_density_line_edit, self.mass_line_edit)
        MainWindow.setTabOrder(self.mass_line_edit, self.ok)
        MainWindow.setTabOrder(self.ok, self.cancel)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Mass Density | Neutron Density | Mass", None))
        self.mass_density_radio_button.setText(_translate("MainWindow", "Mass Density", None))
        self.mass_density_label.setText(_translate("MainWindow", "g/cc", None))
        self.mass_density_error_message.setText(_translate("MainWindow", "Missing Chemical Formula to Update Mass Density!", None))
        self.number_density_radio_button.setText(_translate("MainWindow", "Number Density", None))
        self.number_density_units.setText(_translate("MainWindow", "atom/A", None))
        self.number_density_error_message.setText(_translate("MainWindow", "Missing Chemical Formula to Update Number Density!", None))
        self.label_3.setText(_translate("MainWindow", "Mass", None))
        self.label_4.setText(_translate("MainWindow", "g", None))
        self.label_5.setText(_translate("MainWindow", "geometry:", None))
        self.geometry_label.setText(_translate("MainWindow", "cylindrical", None))
        self.label.setText(_translate("MainWindow", "Volume: ", None))
        self.volume_label.setText(_translate("MainWindow", "N/A", None))
        self.volume_units.setText(_translate("MainWindow", "cm3", None))
        self.mass_error_message.setText(_translate("MainWindow", "Geometry Dimensions Have Not Been Defined! ", None))
        self.cancel.setText(_translate("MainWindow", "Cancel", None))
        self.ok.setText(_translate("MainWindow", "Save", None))

