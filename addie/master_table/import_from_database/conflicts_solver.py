from collections import defaultdict
import numpy as np
import pprint

try:
    from PyQt4.QtGui import QApplication, QMainWindow, QWidget, QTableWidget, QCheckBox, QTableWidgetItem
    from PyQt4 import QtGui, QtCore
except:
    try:
        from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QCheckBox, QTableWidgetItem
        from PyQt5 import QtGui, QtCore
    except:
        raise ImportError("Requires PyQt4 or PyQt5")

from addie.utilities.list_runs_parser import ListRunsParser

from addie.ui_solve_import_conflicts import Ui_MainWindow as UiMainWindow


class ConflictsSolverHandler:

    def __init__(self, parent=None, json_conflicts={}):
        o_solver = ConflictsSolverWindow(parent=parent, json_conflicts=json_conflicts)
        o_solver.show()
        if parent.conflicts_solver_ui_position:
            o_solver.move(parent.conflicts_solver_ui_position)


class ConflictsSolverWindow(QMainWindow):

    list_table = [] # name of table in each of the tabs
    table_width_per_character = 20
    table_header_per_character = 15

    list_keys = ["Run Number", 'chemical_formula', 'geometry', 'mass_density', 'sample_env_device']
    columns_label = ["Run Number", "Chemical Formula", "Geometry", "Mass Density", "Sample Env. Device"]

    def __init__(self, parent=None, json_conflicts={}):
        self.parent = parent
        self.json_conflicts = json_conflicts

        QMainWindow.__init__(self, parent=parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

        self.init_widgets()

    def init_widgets(self):
        json_conflicts = self.json_conflicts

        for _key in json_conflicts.keys():
            if json_conflicts[_key]['any_conflict']:
                self._add_tab(json=json_conflicts[_key]['conflict_dict'])

    def _calculate_columns_width(self, json=None):
        """will loop through all the conflict keys to figure out which one, for each column label, the string
        is the longest"""
        list_key = self.list_keys

        columns_width = defaultdict(list)
        for _key in list_key:
            for _conflict_index in json.keys():
                columns_width[_key].append(self.table_width_per_character * len(json[_conflict_index][_key]))

        final_columns_width = []
        for _key in list_key:
            _max_width = np.max([np.array(columns_width[_key]).max(), len(_key)* self.table_header_per_character])
            final_columns_width.append(_max_width)

        return final_columns_width

    def _add_tab(self, json=None):
        """will look at the json and will display the values in conflicts in a new tab to allow the user
        to fix the conflicts"""

        number_of_tabs = self.ui.tabWidget.count()

        _table = QTableWidget()

        # initialize each table
        columns_width = self._calculate_columns_width(json=json)
        for _col in np.arange(len(json[0])):
            _table.insertColumn(_col)
            _table.setColumnWidth(_col, columns_width[_col])
        for _row in np.arange(len(json)):
            _table.insertRow(_row)
        self.list_table.append(_table)

        _table.setHorizontalHeaderLabels(self.columns_label)

        for _row in np.arange(len(json)):

                # run number
                _col = 0
                list_runs = json[_row]["Run Number"]
                o_parser = ListRunsParser()
                checkbox = QCheckBox(o_parser.new_runs(list_runs=list_runs))
                if _row == 0:
                    checkbox.setChecked(True)
                _table.setCellWidget(_row, _col, checkbox)

                _col += 1
                # chemical formula
                item = QTableWidgetItem(json[_row]["chemical_formula"])
                _table.setItem(_row, _col, item)

                _col += 1
                # geometry
                item = QTableWidgetItem(json[_row]["geometry"])
                _table.setItem(_row, _col, item)

                _col += 1
                # mass_density
                item = QTableWidgetItem(json[_row]["mass_density"])
                _table.setItem(_row, _col, item)

                _col += 1
                # sample_env_device
                item = QTableWidgetItem(json[_row]["sample_env_device"])
                _table.setItem(_row, _col, item)

        self.ui.tabWidget.insertTab(number_of_tabs, _table, "Conflict #{}".format(number_of_tabs))





    def accept(self):
        self.parent.from_oncat_to_master_table(json=self.json_conflicts,
                                               with_conflict=False)

    def reject(self):
        self.parent.from_oncat_to_master_table(json=self.json_conflicts,
                                               ignore_conflicts=True)
        self.close()

    def closeEvent(self, c):
        pass