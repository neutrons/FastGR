import pytest
from qtpy import QtCore, QtWidgets

from addie.menu.file.settings.advanced_file_window import AdvancedWindow
from addie.main import MainWindow


# Utilities / fixtures

def handle_dialog(dialog):
    ''' Handles closing QFileDialog after timer for IDL config tests '''
    while dialog is None:
        QtWidgets.QApplication.processEvents()
    dialog.close()


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
    QtCore.QTimer.singleShot(100, lambda: handle_dialog(advanced_window.ui.idl_config_browse_button_dialog))
    qtbot.mouseClick(
        advanced_window.autonom_path_browse_button,
        QtCore.Qt.LeftButton, delay=1)
    assert advanced_window.parent._autonom_script == target


def test_sum_scans_browse_button(qtbot, advanced_window):
    """ Test the sum scans browse buttons with a file dialog sub-widget """
    target = advanced_window.parent._sum_scans_script
    QtCore.QTimer.singleShot(100, lambda: handle_dialog(advanced_window.ui.idl_config_browse_button_dialog))
    qtbot.mouseClick(
        advanced_window.sum_scans_path_browse_button,
        QtCore.Qt.LeftButton, delay=1)
    assert advanced_window.parent._sum_scans_script == target


def test_ndabs_browse_button(qtbot, advanced_window):
    """ Test the ndabs browse buttons with a file dialog sub-widget """
    target = advanced_window.parent._ndabs_script
    QtCore.QTimer.singleShot(100, lambda: handle_dialog(advanced_window.ui.idl_config_browse_button_dialog))
    qtbot.mouseClick(
        advanced_window.ndabs_path_browse_button,
        QtCore.Qt.LeftButton, delay=1)
    assert advanced_window.parent._ndabs_script == target
