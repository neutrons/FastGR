import os
import pytest
from qtpy import QtCore, QtWidgets

from addie.menu.file.settings.advanced_file_window import AdvancedWindow
from addie.main import MainWindow


# Utilities / fixtures

def close_dialog(dialog):
    ''' Handles closing QFileDialog for IDL config tests '''
    while dialog is None:
        QtWidgets.QApplication.processEvents()
    dialog.close()


def select_and_close_dialog(dialog, directory, filename, delay=0.5):
    ''' Handles selecting and closing QFileDialog for IDL config tests '''

    while dialog is None:
        QtWidgets.QApplication.processEvents()
    # delays to allow files to load in dialog and select file
    # dialog.setDirectory(directory)
    dialog.selectFile(filename)
    dialog.accept()


@pytest.fixture
def main_window(qtbot):
    main_window = MainWindow()
    return main_window


@pytest.fixture
def advanced_window(main_window):
    return AdvancedWindow(main_window)


# Tests

def test_autonom_path_line_edited(advanced_window):
    advanced_window.ui.autonom_path_line_edit.clear()
    advanced_window.autonom_path_line_edited()
    assert advanced_window.parent._autonom_script == ""

    target = "/path/to/script"
    advanced_window.ui.autonom_path_line_edit.setText(target)
    advanced_window.autonom_path_line_edited()
    assert advanced_window.parent._autonom_script == target


def test_sum_scans_path_line_edited(advanced_window):
    advanced_window.ui.sum_scans_path_line_edit.clear()
    advanced_window.sum_scans_path_line_edited()
    assert advanced_window.parent._sum_scans_script == ""

    target = "/path/to/script"
    advanced_window.ui.sum_scans_path_line_edit.setText(target)
    advanced_window.sum_scans_path_line_edited()
    assert advanced_window.parent._sum_scans_script == target


def test_ndabs_path_line_edited(advanced_window):
    advanced_window.ui.ndabs_path_line_edit.clear()
    advanced_window.ndabs_path_line_edited()
    assert advanced_window.parent._ndabs_script == ""

    target = "/path/to/script"
    advanced_window.ui.ndabs_path_line_edit.setText(target)
    advanced_window.ndabs_path_line_edited()
    assert advanced_window.parent._ndabs_script == target


def test_autonom_browse_button(qtbot, advanced_window):
    """ Test the autonom browse buttons with a file dialog sub-widget """
    target = advanced_window.parent._autonom_script
    QtCore.QTimer.singleShot(
        100,
        lambda: close_dialog(
            advanced_window.ui.idl_config_browse_button_dialog))
    qtbot.mouseClick(
        advanced_window.autonom_path_browse_button,
        QtCore.Qt.LeftButton, delay=1)
    assert advanced_window.parent._autonom_script == target

    directory = os.path.abspath('.')
    filename = 'setup.py'
    target = os.path.join(directory, filename)
    QtCore.QTimer.singleShot(
        10,
        lambda: select_and_close_dialog(
            advanced_window.ui.idl_config_browse_button_dialog,
            directory,
            filename))
    qtbot.mouseClick(
        advanced_window.autonom_path_browse_button,
        QtCore.Qt.LeftButton, delay=1)
    assert advanced_window.parent._autonom_script == target


def test_sum_scans_browse_button(qtbot, advanced_window):
    """ Test the sum scans browse buttons with a file dialog sub-widget """
    target = advanced_window.parent._sum_scans_script
    QtCore.QTimer.singleShot(
        100,
        lambda: close_dialog(
            advanced_window.ui.idl_config_browse_button_dialog))
    qtbot.mouseClick(
        advanced_window.sum_scans_path_browse_button,
        QtCore.Qt.LeftButton, delay=1)
    assert advanced_window.parent._sum_scans_script == target

    directory = os.path.abspath('.')
    filename = 'setup.py'
    target = os.path.join(directory, filename)
    QtCore.QTimer.singleShot(
        10,
        lambda: select_and_close_dialog(
            advanced_window.ui.idl_config_browse_button_dialog,
            directory,
            filename))
    qtbot.mouseClick(
        advanced_window.sum_scans_path_browse_button,
        QtCore.Qt.LeftButton, delay=1)
    assert advanced_window.parent._sum_scans_script == target


def test_ndabs_browse_button(qtbot, advanced_window):
    """ Test the ndabs browse buttons with a file dialog sub-widget """
    target = advanced_window.parent._ndabs_script
    QtCore.QTimer.singleShot(
        100,
        lambda: close_dialog(
            advanced_window.ui.idl_config_browse_button_dialog))
    qtbot.mouseClick(
        advanced_window.ndabs_path_browse_button,
        QtCore.Qt.LeftButton, delay=1)
    assert advanced_window.parent._ndabs_script == target

    directory = os.path.abspath('.')
    filename = 'setup.py'
    target = os.path.join(directory, filename)
    QtCore.QTimer.singleShot(
        10,
        lambda: select_and_close_dialog(
            advanced_window.ui.idl_config_browse_button_dialog,
            directory,
            filename))
    qtbot.mouseClick(
        advanced_window.ndabs_path_browse_button,
        QtCore.Qt.LeftButton, delay=1)
    assert advanced_window.parent._ndabs_script == target


def test_sum_scans_python_version_checkbox_toggled(qtbot, advanced_window):
    """ Test the sum scans python version checkbox works """
    checkbox = advanced_window.sum_scans_python_version_checkbox
    initialState = advanced_window.parent._is_sum_scans_python_checked

    qtbot.mouseClick(checkbox, QtCore.Qt.LeftButton)
    assert checkbox.isChecked() != initialState
    assert advanced_window.parent._is_sum_scans_python_checked != initialState

    qtbot.mouseClick(checkbox, QtCore.Qt.LeftButton)
    assert checkbox.isChecked() == initialState
    assert advanced_window.parent._is_sum_scans_python_checked == initialState
