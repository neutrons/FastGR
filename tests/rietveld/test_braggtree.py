from __future__ import absolute_import, print_function
import pytest
import os
import addie.rietveld.event_handler
from tests import DATA_DIR

from addie.rietveld.braggtree import BraggTree, BankRegexException
from addie.main import MainWindow


@pytest.fixture
def bragg_tree():
    main_window = MainWindow()
    return BraggTree(main_window)


def test_add_bragg_ws_group(qtbot, bragg_tree):
    ws_group_name = "WorkspaceGroup"
    bank_angles = [20, 30, 90]
    bank_list = list()
    for i, angle in enumerate(bank_angles):
        bank_list.append('Bank {} - {}'.format(i + 1, angle))
    bragg_tree.add_bragg_ws_group(ws_group_name, bank_list)


def test_get_bank_id(qtbot, bragg_tree):
    """Test we can extract a bank id from bank workspace name"""
    target = 12345
    bank_wksp_name = "Bank {} - 90.0".format(target)
    bank_id = bragg_tree._get_bank_id(bank_wksp_name)
    assert int(bank_id) == target


def test_get_bank_id_exception(qtbot, bragg_tree):
    """Test for raised exception from a bad workspace name"""
    bad_ws = "Bank jkl 1 -- 90.0"
    with pytest.raises(BankRegexException):
        bragg_tree._get_bank_id(bad_ws)


def test_do_plot_ws(qtbot, bragg_tree):
    """Test for plotting selected bank workspace"""
    filename = 'NOM_127827.gsa'
    filename = os.path.join(DATA_DIR, filename)
    print(bragg_tree.currentIndex())
    #bragg_tree.setCurrentIndex(0)
    wksp, angles = addie.rietveld.event_handler.load_bragg_by_filename(filename)
    bragg_tree.do_plot_ws()


def test_do_plot_ws_exception(qtbot):
    """Test for raised exception from MainWindow==None"""
    bragg_tree = BraggTree(None)
    with pytest.raises(NotImplementedError):
        bragg_tree.do_plot_ws()
