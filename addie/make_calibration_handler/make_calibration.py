from PyQt4 import QtGui, QtCore
import datetime
from collections import namedtuple
import os

from addie.ui_make_calibration import Ui_MainWindow as UiMainWindow
from addie.utilities.gui_handler import TableHandler


class MakeCalibrationLauncher(object):

    def __init__(self, parent=None):
        self.parent = parent

        if self.parent.make_calibration_ui is None:
            _make = MakeCalibrationWindow(parent=self.parent)
            _make.show()
            self.parent.make_calibration_ui = _make
        else:
            self.parent.make_calibration_ui.setFocus()
            self.parent.make_calibration_ui.activateWindow()


class MakeCalibrationWindow(QtGui.QMainWindow):

    table_column_width = [60, 350, 350, 90, 300]
    table_row_height = 85
    entry_level =  0

    master_date = None  #QtCore.QDate()
    master_folder = 'N/A'

    # will keep record of all the ui
    local_list_ui = namedtuple("local_list_ui", ["calibration_run_radio_button",
                                                 "calibration_value",
                                                 "calibration_browser",
                                                 "calibration_browser_value",
                                                 "calibration_browser_radio_button",
                                                 "vanadium_run_radio_button",
                                                 "vanadium_value",
                                                 "vanadium_browser_radio_button",
                                                 "vanadium_browser",
                                                 "vanadium_browser_value",
                                                 "date",
                                                 "output_dir_browser",
                                                 "output_dir_value",
                                                 "output_reset"])

    master_list_ui = {}
    master_list_value = {}

    def __init__(self, parent=None):
        self.parent = parent

        QtGui.QMainWindow.__init__(self, parent=parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        self.init_widgets()
        self.init_date()
        self.update_add_remove_widgets()

    def init_date(self):
        """will initialize the master date using today's date"""
        now = datetime.datetime.now()
        day = now.day
        month = now.month
        year = now.year
        today = QtCore.QDate(year, month, day)
        self.master_date = today
        self.ui.master_date.setDate(today)

    def init_widgets(self):
        for index_col, col_size in enumerate(self.table_column_width):
            self.ui.tableWidget.setColumnWidth(index_col, col_size)

    def update_add_remove_widgets(self):
        nbr_row = self.ui.tableWidget.rowCount()
        if nbr_row > 0:
            _status = True
        else:
            _status = False
        self.ui.remove_row_button.setEnabled(_status)

    def master_browse_button_clicked(self):
        _master_folder = QtGui.QFileDialog.getExistingDirectory(caption="Select Output Folder ...",
                                                                directory=self.parent.output_folder,
                                                                options=QtGui.QFileDialog.ShowDirsOnly)
        if _master_folder:
            self.ui.master_output_directory_label.setText(str(_master_folder))
            self.master_folder = _master_folder

    def remove_row_button_clicked(self):
        o_gui = TableHandler(table_ui=self.ui.tableWidget)
        row_selected = o_gui.get_current_row()

        # no row selected
        if row_selected == -1:
            return

        entry = str(self.ui.tableWidget.item(row_selected, 0).text())
        self.ui.tableWidget.removeRow(row_selected)
        # remove list of ui from this row
        del self.master_list_ui[entry]
        self.update_add_remove_widgets()

    def add_row_button_clicked(self):
        o_gui = TableHandler(table_ui=self.ui.tableWidget)
        row_selected = o_gui.get_current_row()
        self.__insert_new_row(row=row_selected+1)
        self.update_add_remove_widgets()

    def _general_browser_clicked(self,
                                 sample_type='',
                                 browser_radio_button_ui=None,
                                 value_ui=None):
        _file = QtGui.QFileDialog.getOpenFileName(parent=self,
                                                  caption="Select {} File ...".format(sample_type),
                                                  directory=self.master_folder,
                                                  filter="NeXus (*.nxs);; All (*.*)")
        if _file:
            # enable the radio button
            browser_radio_button_ui.setChecked(True)
            # display base name of file selected (without path)
            value_ui.setText(os.path.basename(_file))
            return _file


    def vanadium_browser_clicked(self, entry=""):
        sample_type = "Vanadium"
        browser_radio_button_ui = self.master_list_ui[entry].vanadium_browser_radio_button
        value_ui = self.master_list_ui[entry].vanadium_browser_value

        _file = self._general_browser_clicked(sample_type=sample_type,
                                              browser_radio_button_ui=browser_radio_button_ui,
                                              value_ui=value_ui)
        if _file:
            self.master_list_value[entry]["vanadium_browser"] = _file

    def calibration_browser_clicked(self, entry=""):
        sample_type = "Calibration"
        browser_radio_button_ui = self.master_list_ui[entry].calibration_browser_radio_button
        value_ui = self.master_list_ui[entry].calibration_browser_value

        _file = self._general_browser_clicked(sample_type=sample_type,
                                              browser_radio_button_ui=browser_radio_button_ui,
                                              value_ui=value_ui)
        if _file:
            self.master_list_value[entry]["calibration_browser"] = _file

    def local_output_dir_clicked(self, entry=""):
        _local_folder = QtGui.QFileDialog.getExistingDirectory(caption="Select Output Folder ...",
                                                                directory=self.master_folder,
                                                                options=QtGui.QFileDialog.ShowDirsOnly)
        if _local_folder:
            _master_list_ui = self.master_list_ui[entry]
            _local_label = _master_list_ui.output_dir_value
            _local_label.setText(str(_local_folder))

    def local_reset_dir_clicked(self, entry=""):
        _master_list_ui = self.master_list_ui[entry]
        _local_label = _master_list_ui.output_dir_value
        _local_label.setText(str(self.master_folder))

    def __insert_new_row(self, row=-1):
        self.ui.tableWidget.insertRow(row)
        self.ui.tableWidget.setRowHeight(row, self.table_row_height)

        button_width = 80

        new_entry_level = self.entry_level + 1
        self.entry_level = new_entry_level

        #column0 - entry
        _name = str(new_entry_level)
        item = QtGui.QTableWidgetItem(str(_name))
        self.ui.tableWidget.setItem(row, 0, item)

        #column 1 - calibration
        # first row
        cali_run_radio_button = QtGui.QRadioButton()
        cali_run_radio_button.setChecked(True)
        label = QtGui.QLabel("Run #:")
        cali_value = QtGui.QLineEdit("")
        # second row
        cali_browser_radio_button = QtGui.QRadioButton()
        cali_browser_button = QtGui.QPushButton("Browse...")
        cali_browser_button.setMinimumWidth(button_width)
        cali_browser_button.setMaximumWidth(button_width)
        cali_browser_button.clicked.connect(lambda state, entry=_name:  self.calibration_browser_clicked(entry))
        cali_browser_button_value = QtGui.QLabel("N/A")

        grid_layout = QtGui.QGridLayout()
        grid_layout.addWidget(cali_run_radio_button, 0, 0)
        grid_layout.addWidget(label, 0, 1)
        grid_layout.addWidget(cali_value, 0, 2)

        grid_layout.addWidget(cali_browser_radio_button, 1, 0)
        grid_layout.addWidget(cali_browser_button, 1, 1)
        grid_layout.addWidget(cali_browser_button_value, 1, 2)

        col1_widget = QtGui.QWidget()
        col1_widget.setLayout(grid_layout)
        self.ui.tableWidget.setCellWidget(row, 1, col1_widget)

        #column 2 - Vanadium
        # first row
        vana_run_radio_button = QtGui.QRadioButton()
        vana_run_radio_button.setChecked(True)
        label = QtGui.QLabel("Run #:")
        vana_value = QtGui.QLineEdit("")
        # second row
        vana_browser_radio_button = QtGui.QRadioButton()
        vana_browser_button = QtGui.QPushButton("Browse...")
        vana_browser_button.setMinimumWidth(button_width)
        vana_browser_button.setMaximumWidth(button_width)
        vana_browser_button.clicked.connect(lambda state, entry=_name:  self.vanadium_browser_clicked(entry))
        vana_browser_button_value = QtGui.QLabel("N/A")

        grid_layout = QtGui.QGridLayout()
        grid_layout.addWidget(vana_run_radio_button, 0, 0)
        grid_layout.addWidget(label, 0, 1)
        grid_layout.addWidget(vana_value, 0, 2)

        grid_layout.addWidget(vana_browser_radio_button, 1, 0)
        grid_layout.addWidget(vana_browser_button, 1, 1)
        grid_layout.addWidget(vana_browser_button_value, 1, 2)

        col1_widget = QtGui.QWidget()
        col1_widget.setLayout(grid_layout)
        self.ui.tableWidget.setCellWidget(row, 2, col1_widget)

        #column 3 - date
        date = QtGui.QDateEdit()
        date.setDate(self.master_date)
        self.ui.tableWidget.setCellWidget(row, 3, date)

        #column 4 - output dir
        browser_button = QtGui.QPushButton("Browse...")
        browser_button.setMinimumWidth(button_width)
        browser_button.setMaximumWidth(button_width)
        browser_button.clicked.connect(lambda state, entry=_name: self.local_output_dir_clicked(entry))
        value = QtGui.QLabel(self.master_folder)
        reset = QtGui.QPushButton("Use Master")
        reset.setMinimumWidth(button_width)
        reset.setMaximumWidth(button_width)
        reset.clicked.connect(lambda state, entry=_name: self.local_reset_dir_clicked(entry))
        hori_layout = QtGui.QHBoxLayout()
        hori_layout.addWidget(browser_button)
        hori_layout.addWidget(value)
        hori_layout.addWidget(reset)
        widget = QtGui.QWidget()
        widget.setLayout(hori_layout)
        self.ui.tableWidget.setCellWidget(row, 4, widget)

        list_local_ui = self.local_list_ui(calibration_run_radio_button=cali_run_radio_button,
                                           calibration_value=cali_value,
                                           calibration_browser=cali_browser_button,
                                           calibration_browser_value=cali_browser_button_value,
                                           calibration_browser_radio_button=cali_browser_radio_button,
                                           vanadium_run_radio_button=vana_run_radio_button,
                                           vanadium_value=vana_value,
                                           vanadium_browser_radio_button=vana_browser_radio_button,
                                           vanadium_browser=vana_browser_button,
                                           vanadium_browser_value=vana_browser_button_value,
                                           date=date,
                                           output_dir_browser=browser_button,
                                           output_dir_value=value,
                                           output_reset=reset)
        self.master_list_ui[_name] = list_local_ui

        list_local_name = dict(vanadium_run_number="",
                               vanadium_browser="",
                               calibration_run_number="",
                               calibration_browser="")
        self.master_list_value[_name] = list_local_name

    def run_calibration_button_clicked(self):
        print("run calibration")

    def closeEvent(self, c):
        self.parent.make_calibration_ui = None

