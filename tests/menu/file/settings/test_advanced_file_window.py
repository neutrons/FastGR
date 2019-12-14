import pytest
from qtpy import QtCore, QtWidgets

from addie.menu.file.settings.advanced_file_window import AdvancedWindow
from addie.main import MainWindow


@pytest.fixture
def main_window(qtbot):
    main_window = MainWindow()
    return main_window


@pytest.fixture
def advanced_window(main_window):
    return AdvancedWindow(main_window)


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


def test_idl_button_clicked(qtbot, advanced_window):
    """ Test the browse button function with a file dialog sub-widget """
    # Handles closing the file dialog sub-widget after timer
    def handle_dialog():
        while advanced_window.ui.idl_config_browse_button_dialog is None:
            QtWidgets.QApplication.processEvents()
        advanced_window.ui.idl_config_browse_button_dialog.close()

    # Setup closing the file diloag after 100 ms after left click on browse button
    QtCore.QTimer.singleShot(1000, handle_dialog)
    qtbot.mouseClick(advanced_window.autonom_path_browse_button, QtCore.Qt.LeftButton, delay=1)
