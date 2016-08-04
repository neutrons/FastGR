#!/usr/bin/env python

import sys
import os
from fastgr.ipythondockwidget import IPythonDockWidget

import fastgr.ui_mainWindow
import fastgr.step1
import fastgr.step2

from fastgr.initialization.init_step1 import InitStep1
from fastgr.step1_handler.step1_gui_handler import Step1GuiHandler
from fastgr.step1_handler.run_step1 import RunStep1

from fastgr.initialization.init_step2 import InitStep2
from fastgr.step2_handler.populate_master_table import PopulateMasterTable
from fastgr.step2_handler.populate_background_widgets import PopulateBackgroundWidgets
from fastgr.step2_handler.step2_gui_handler import Step2GuiHandler
from fastgr.step2_handler.table_handler import TableHandler
from fastgr.step2_handler.create_sample_files import CreateSampleFiles
from fastgr.step2_handler.create_ndsum_file import CreateNdsumFile
from fastgr.step2_handler.run_ndabs import RunNDabs
from fastgr.step2_handler.run_sum_scans import RunSumScans
from fastgr.step3_handler.step3_gui_handler import Step3GuiHandler

import PyQt4
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

import fastgr.fastgrdriver as driver

__version__ = "1.0.0"


class MainWindow(PyQt4.QtGui.QMainWindow, fastgr.ui_mainWindow.Ui_MainWindow):
    """ Main FastGR window
    """
    debugging = False
    current_folder = os.getcwd()
    table_selection_buffer = {}

    def __init__(self):
        """ Initialization
        Parameters
        ----------
        parent :: parent application
        """

        # Base class
        QtGui.QMainWindow.__init__(self)

        # Initialize the UI widgets
        self.ui = fastgr.ui_mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.graphicsView_sq.set_main(self)
 
        self.ui.dockWidget_ipython.setup()

        # set widgets
        self._init_widgets()
        init_step1 = InitStep1(parent=self)
        init_step2 = InitStep2(parent=self)

        # define the event handling methods

        # bragg diffraction tab
        self.connect(self.ui.pushButton_loadBraggFile, QtCore.SIGNAL('clicked()'),
                     self.do_load_bragg_file)
        self.connect(self.ui.checkBox_bank1, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank2, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank3, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank4, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank5, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.checkBox_bank6, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.comboBox_xUnit, QtCore.SIGNAL('currentIndexChanged(int)'),
                     self.evt_plot_bragg_bank)
        self.connect(self.ui.radioButton_multiBank, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_change_gss_mode)

        # for tab G(R)
        self.connect(self.ui.pushButton_loadSQ, QtCore.SIGNAL('clicked()'),
                     self.do_load_sq)
        self.connect(self.ui.radioButton_sq, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_sq)
        self.connect(self.ui.radioButton_sqm1, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_sq)
        self.connect(self.ui.radioButton_qsqm1, QtCore.SIGNAL('toggled(bool)'),
                     self.evt_plot_sq)
        self.connect(self.ui.pushButton_clearSofQ, QtCore.SIGNAL('clicked()'),
                     self.do_clear_sq)
        self.connect(self.ui.pushButton_showQMinMax, QtCore.SIGNAL('clicked()'),
                     self.do_show_sq_bound)
        self.connect(self.ui.pushButton_generateGR, QtCore.SIGNAL('clicked()'),
                     self.do_generate_gr)
        self.connect(self.ui.pushButton_loadGofR, QtCore.SIGNAL('clicked()'),
                     self.do_load_gr)
        self.connect(self.ui.pushButton_saveGR, QtCore.SIGNAL('clicked()'),
                     self.do_save_gr)
        self.connect(self.ui.pushButton_clearGrCanvas, QtCore.SIGNAL('clicked()'),
                     self.do_clear_gr)

        self.connect(self.ui.doubleSpinBoxQmin, QtCore.SIGNAL('valueChanged(double)'),
                     self.evt_qmin_changed)
        self.connect(self.ui.doubleSpinBoxQmax, QtCore.SIGNAL('valueChanged(double)'),
                     self.evt_qmax_changed)

        #  menu operations
        self.connect(self.ui.actionReset_GofR_tab, QtCore.SIGNAL('triggered()'),
                     self.do_reset_gr_tab)
        self.connect(self.ui.actionReset_GSAS_tab, QtCore.SIGNAL('triggered()'),
                     self.do_reset_gsas_tab)
        self.connect(self.ui.actionQuit, QtCore.SIGNAL('triggered()'),
                     self.evt_quit)

        # organize widgets group
        self._braggBankWidgets = {1: self.ui.checkBox_bank1,
                                  2: self.ui.checkBox_bank2,
                                  3: self.ui.checkBox_bank3,
                                  4: self.ui.checkBox_bank4,
                                  5: self.ui.checkBox_bank5,
                                  6: self.ui.checkBox_bank6}
        self._braggBankWidgetRecords = dict()
        for bank_id in self._braggBankWidgets.keys():
            checked = self._braggBankWidgets[bank_id].isChecked()
            self._braggBankWidgetRecords[bank_id] = checked

        # define the driver
        self._myController = driver.FastGRDriver()

        # class variable for easy access
        self._gssGroupName = None
        self._currDataDir = None

        # some controlling variables
        self._currBraggXUnit = str(self.ui.comboBox_xUnit.currentText())

        # mutex-like variables
        self._noEventBankWidgets = False

        return

    def _init_widgets(self):
        """ Initialize widgets
        Returns
        -------

        """
        self.ui.comboBox_xUnit.clear()
        self.ui.comboBox_xUnit.addItems(['TOF', 'dSpacing', 'Q'])

        self.ui.treeWidget_braggWSList.set_main_window(self)
        self.ui.treeWidget_braggWSList.add_main_item('workspaces', append=True, as_current_index=False)

        self.ui.treeWidget_grWsList.set_main_window(self)
        self.ui.treeWidget_grWsList.add_main_item('workspaces', append=True, as_current_index=False)
        self.ui.treeWidget_grWsList.add_main_item('SofQ', append=True, as_current_index=False)

        self.ui.dockWidget_ipython.iPythonWidget.set_main_application(self)

        self.ui.radioButton_sq.setChecked(True)
        self.ui.radioButton_multiBank.setChecked(True)

        # add the combo box for PDF type
        self.ui.comboBox_pdfType.addItems(['G(r)', 'g(r)', 'RDF(r)'])

        # some starting value
        self.ui.doubleSpinBoxDelR.setValue(0.01)

        return

    def do_clear_gr(self):
        """
        Clear G(r) canvas
        Returns
        -------

        """
        self.ui.graphicsView_gr.clear_all_lines()

        return

    def do_clear_sq(self):
        """
        Clear S(Q) canvas
        Returns
        -------

        """
        self.ui.graphicsView_sq.clear_all_lines()

        return

    def do_generate_gr(self):
        """
        Generate G(r) by the present user-setup
        Returns
        -------

        """
        # get S(Q) workspace
        sq_ws_name = str(self.ui.comboBox_SofQ.currentText())

        # get r-range and q-range
        min_r = float(self.ui.doubleSpinBoxRmin.value())
        max_r = float(self.ui.doubleSpinBoxRmax.value())
        delta_r = float(self.ui.doubleSpinBoxDelR.value())

        min_q = float(self.ui.doubleSpinBoxQmin.value())
        max_q = float(self.ui.doubleSpinBoxQmax.value())

        # PDF type
        pdf_type = str(self.ui.comboBox_pdfType.currentText())

        # calculate the G(R)
        gr_ws_name = self._myController.calculate_gr(sq_ws_name, pdf_type, min_r, delta_r, max_r,
                                                     min_q, max_q)

        # plot G(R)
        vec_r, vec_g, vec_ge = self._myController.get_gr(min_q, max_q)
        key_plot = gr_ws_name
        self.ui.graphicsView_gr.plot_gr(key_plot, vec_r, vec_g, vec_ge, False)

        # add to tree
        gr_param_str = 'Q: (%.3f, %.3f)' % (min_q, max_q)
        self.ui.treeWidget_grWsList.add_gr(gr_param_str, gr_ws_name)

        return

    def do_reset_gr_tab(self):
        """
        Reset G(r)-tab, including deleting all the G(r) and S(Q) workspaces,
        clearing the G(r) and S(Q) trees, and clearing both G(r) and S(Q) canvas
        Returns:
        None
        """
        # get workspace from trees
        workspace_list = self.ui.treeWidget_grWsList.get_workspaces()

        # reset the tree to initial status
        self.ui.treeWidget_grWsList.reset_gr_tree()

        # delete all the workspaces
        for workspace in workspace_list:
            self._myController.delete_workspace(workspace)

        # clear all the canvas
        self.ui.graphicsView_gr.clear_all_lines()
        self.ui.graphicsView_sq.clear_all_lines()

        return

    def do_reset_gsas_tab(self):
        """
        Reset the GSAS-tab including
        1. deleting all the GSAS workspaces
        2. clearing the GSAS tree
        3. clearing GSAS canvas
        Returns:
        None
        """
        # delete all workspaces: get GSAS workspaces from tree
        # TODO/FIXME/ISSUE 5 : delete all the workspaces related
        blablabla
        # gsas_ws_list = self.ui.treeWidget_braggWSList.GET_WORKSPACES()
        # for workspace in gsas_ws_list:
        #     self._myController.delete_workspace(workspace)

        # reset the GSAS tree
        self.ui.treeWidget_braggWSList.reset_bragg_tree()

        # clear the canvas
        self.ui.graphicsView_bragg.reset()

        # TODO/FIXME/ISSUE 5: clear the checkboxes for banks
        blablabla

        return

    def plot_bragg(self, bragg_ws_list, clear_canvas=False):
        """

        Parameters
        ----------
        bragg_ws_list: list of (single spectrum) Bragg workspace
        clear_canvas

        Returns
        -------

        """
        # check
        assert isinstance(bragg_ws_list, list)

        # clear canvas if necessary
        if clear_canvas:
            self.ui.graphicsView_bragg.reset()

        # get unit
        curr_unit = str(self.ui.comboBox_xUnit.currentText())

        # plot all workspsaces
        print '[DB...BAT] Bragg ws list: ', bragg_ws_list
        for bragg_ws_name in bragg_ws_list:

            # get the last section of the workspace name: _bank%d
            postfix = bragg_ws_name.split('_')[-1]

            if postfix.startswith('bank') and 0 <= int(postfix.split('bank')[1]) <= 6:
                # belonged to a Bragg-workspace-group
                ws_group = bragg_ws_name.split('_%s' % postfix)[0] + '_group'
                bank_id = int(bragg_ws_name.split('bank')[1])
                vec_x, vec_y, vec_e = self._myController.get_bragg_data(ws_group_name=ws_group, bank_id=bank_id,
                                                                        x_unit=curr_unit)

                # construct dictionary for plotting
                plot_data_dict = dict()
                plot_data_dict[ws_group] = dict()
                plot_data_dict[ws_group][bank_id] = (vec_x, vec_y, vec_e)

                # set the bank to be checked
                self._braggBankWidgets[bank_id].setChecked(True)

                # plot
                self.ui.graphicsView_bragg.plot_banks(plot_data_dict, curr_unit)

            else:
                vec_x, vec_y, vec_e = self._myController.get_ws_data(bragg_ws_name)
                self.ui.graphicsView_bragg.plot_general_ws(bragg_ws_name, vec_x, vec_y, vec_e)

        return

    def plot_gr(self, gr_ws_name_list):
        """
        Plot G(r) by their names (workspace as protocol)
        Parameters
        ----------
        gr_ws_name_list: list of G(r) workspaces

        Returns
        -------

        """
        # check
        assert isinstance(gr_ws_name_list, list) and len(gr_ws_name_list) > 0

        # plot G(R)
        for gr_ws_name in gr_ws_name_list:
            vec_r, vec_g, vec_ge = self._myController.get_gr_by_ws(gr_ws_name)
            key_plot = gr_ws_name
            self.ui.graphicsView_gr.plot_gr(key_plot, vec_r, vec_g, vec_ge, False)

        return

    def plot_sq(self, sq_ws_name, clear_prev):
        """
        Plot S(Q)
        Parameters
        ----------
        sq_ws_name
        clear_prev

        Returns
        -------

        """
        # clear previous lines
        if clear_prev:
            self.ui.graphicsView_sq.clear_all_lines()

        # get data
        vec_q, vec_sq, vec_se = self._myController.get_sq(sq_ws_name)

        # get the unit & do conversion if necessary
        if self.ui.radioButton_sq.isChecked():
            # use the original S(Q)
            sq_unit = 'S(Q)'
            vec_y = vec_sq
        elif self.ui.radioButton_sqm1.isChecked():
            # use S(Q)-1
            sq_unit = 'S(Q)-1'
            vec_y = vec_sq - 1
        elif self.ui.radioButton_qsqm1.isChecked():
            # use Q(S(Q)-1)
            sq_unit = 'Q(S(Q)-1)'
            vec_y = vec_q * (vec_sq - 1)
        else:
            raise RuntimeError('None of S(Q), S(Q)-1 or Q(S(Q)-1) is chosen.')

        # plot
        if clear_prev:
            reset = True
        else:
            reset = False
        self.ui.graphicsView_sq.plot_sq(sq_ws_name, vec_q, vec_y, vec_se, sq_unit, reset)

        return

    def do_load_bragg_file(self):
        """
        Load Bragg files including GSAS, NeXus, 3-column ASCii.
        Returns
        -------
        """
        # get file
        ext = 'GSAS (*.gsa);;DAT (*.dat);;All (*.*)'

        # get default dir
        if self._currDataDir is None:
            default_dir = os.getcwd()
        else:
            default_dir = self._currDataDir

        bragg_file_name = str(QtGui.QFileDialog.getOpenFileName(self, 'Choose Bragg File', default_dir, ext))
        if bragg_file_name is None or bragg_file_name == '':
            return

        # update stored data directory
        self._currDataDir = os.path.abspath(bragg_file_name)

        # load file
        gss_ws_name = self._myController.load_bragg_file(bragg_file_name)

        # split
        self._gssGroupName, banks_list, bank_angles = self._myController.split_to_single_bank(gss_ws_name)

        # add to tree
        self.ui.treeWidget_braggWSList.add_bragg_ws_group(self._gssGroupName, banks_list)

        # rename bank
        for bank_id in self._braggBankWidgets.keys():
            bank_check_box = self._braggBankWidgets[bank_id]

            if bank_id > len(bank_angles) or bank_angles[bank_id-1] is None:
                bank_check_box.setText('Bank %d' % bank_id)
            else:
                bank_check_box.setText('Bank %.1f' % bank_angles[bank_id-1])

        # clear all lines
        self.ui.graphicsView_bragg.reset()

        # un-check all the check boxes with mutex on and off
        self._noEventBankWidgets = True
        for check_box in self._braggBankWidgets.values():
            check_box.setChecked(False)
        self._noEventBankWidgets = False

        # plot and will triggered the graph
        self.ui.checkBox_bank1.setChecked(True)

        return

    def do_load_gr(self):
        """
        Load an ASCII file containing G(r)
        Returns:
        """
        # get default dir
        if self._currDataDir is None:
            default_dir = os.getcwd()
        else:
            default_dir = self._currDataDir

        # pop out file
        file_filter = 'Data Files (*.data);;All Files (*.*)'
        g_file_name = str(QtGui.QFileDialog.getOpenFileName(self, 'Open a G(r) file', default_dir, file_filter))

        # return if operation is cancelled
        if g_file_name is None or g_file_name == '':
            return
        else:
            # update current data directory
            self._currDataDir = os.path.abspath(g_file_name)

        # read file
        status, ret_obj = self._myController.load_gr(g_file_name)
        if not status:
            err_msg = ret_obj
            print err_msg
            return
        else:
            gr_ws_name = ret_obj

        # plot
        self.plot_gr([gr_ws_name])

        # TODO/FIXME/ISSUE 5: put the loaded G(r) workspace to tree 'workspaces'
        blablabla

        return

    def do_load_sq(self):
        """
        Load S(Q) from file
        Returns
        -------

        """
        # get default dir
        if self._currDataDir is None:
            default_dir = os.getcwd()
        else:
            default_dir = self._currDataDir

        # get the file
        ext = 'DAT (*.dat);;All (*.*)'
        sq_file_name = str(QtGui.QFileDialog.getOpenFileName(self, 'Choose S(Q) File', default_dir, ext))
        if sq_file_name is None or sq_file_name == '':
            return
        else:
            # update current data directory
            self._currDataDir = os.path.abspath(sq_file_name)

        # load S(q)
        sq_ws_name, q_min, q_max = self._myController.load_sq(sq_file_name)

        # set to the tree and combo box
        self.ui.treeWidget_grWsList.add_sq(sq_ws_name)
        self.ui.comboBox_SofQ.addItem(sq_ws_name)
        self.ui.comboBox_SofQ.setCurrentIndex(self.ui.comboBox_SofQ.count()-1)

        # set the UI widgets
        self.ui.doubleSpinBoxQmin.setValue(q_min)
        self.ui.doubleSpinBoxQmax.setValue(q_max)

        # plot the figure
        self.evt_plot_sq()

        # calculate and calculate G(R)
        self.do_generate_gr()

        return

    def do_save_gr(self):
        """
        Save the selected the G(r) from menu to ASCII file
        Returns
        -------

        """
        # read the selected item from the tree
        gr_name_list = self.ui.treeWidget_grWsList.get_selected_items_of_level(2, excluded_parent='SofQ',
                                                                               return_item_text=True)
        if len(gr_name_list) != 1:
            self.pop_message('Error! Only 1 workspace of G(r) that can be selected.  So far %d'
                             ' is selected.' % len(gr_name_list))
            return
        else:
            gr_ws_name = gr_name_list[0]

        print '[DB...BAT] G(r) workspace: %s' % gr_ws_name

        # pop-up a dialog for the file to save
        default_dir = os.getcwd()
        file_ext = 'Data (*.dat)'
        gr_file_name = str(QtGui.QFileDialog.getSaveFileName(self, caption='Save G(r)',
                                                             directory=default_dir, filter=file_ext))

        # save!
        self._myController.save_ascii(gr_ws_name, gr_file_name)

        return

    def do_show_sq_bound(self):
        """
        Show or hide the left and right boundary of the S(Q)
        Returns
        -------

        """
        q_left = self.ui.doubleSpinBoxQmin.value()
        q_right = self.ui.doubleSpinBoxQmax.value()
        self.ui.graphicsView_sq.toggle_boundary(q_left, q_right)

        return

    def get_bragg_banks_selected(self):
        """
        Find out the banks of bragg-tab that are selected.
        Returns:

        """
        bank_id_list = list()
        for bank_id in self._braggBankWidgets.keys():
            # access the checkbox
            bank_checkbox = self._braggBankWidgets[bank_id]
            # append
            if bank_checkbox.isChecked():
                bank_id_list.append(bank_id)
        # END-FOR

        return bank_id_list

    def evt_change_gss_mode(self):
        """

        Returns
        -------

        """
        # check the mode (multiple bank or multiple GSS)
        single_gss_mode = self.ui.radioButton_multiBank.isChecked()
        assert single_gss_mode != self.ui.radioButton_multiGSS.isChecked()

        # get the banks that are selected
        to_plot_bank_list = self.get_bragg_banks_selected()
        on_canvas_ws_list = self.ui.graphicsView_bragg.get_workspaces()
        # return with doing anything if the canvas is empty, i.e., no bank is selected
        if len(to_plot_bank_list) == 0:
            return
        # return if there is no workspace that is plotted on canvas now
        if len(on_canvas_ws_list) == 0:
            return

        # set to single GSS
        self.ui.graphicsView_bragg.set_to_single_gss(single_gss_mode)

        # process the plot with various situation
        if single_gss_mode:
            # switch to single GSAS mode from multiple GSAS mode.
            #  select the arbitrary gsas file to
            assert len(to_plot_bank_list) == 1

            # skip if there is one and only one workspace
            if len(on_canvas_ws_list) == 1:
                return
            else:
                plot_ws_name = on_canvas_ws_list[0]

            # plot
            bragg_bank_ws = '%s_bank%d' % (plot_ws_name, to_plot_bank_list[0])
            self.plot_bragg(bragg_ws_list=[bragg_bank_ws], clear_canvas=True)

        else:
            # multiple GSAS mode. as currently there is one GSAS file that is plot, then the first bank
            # that is plotted will be kept on the canvas
            # assumption: switched from single-bank mode
            assert len(self.ui.graphicsView_bragg.get_workspaces()) == 1

            # skip if there is one and only 1 bank that is selected
            if len(to_plot_bank_list) == 1:
                return
            else:
                # choose first bank
                bank_to_plot = to_plot_bank_list[0]

            # disable all the banks except the one to plot. Notice the mutex must be on
            self._noEventBankWidgets = True
            for bank_id in self._braggBankWidgets.keys():
                if bank_id != bank_to_plot:
                    self._braggBankWidgets[bank_id].setChecked(False)
            self._noEventBankWidgets = False

            # plot
            plot_ws_name = on_canvas_ws_list[0]
            bragg_bank_ws = '%s_bank%d' % (plot_ws_name, bank_to_plot)
            self.plot_bragg(bragg_ws_list=[bragg_bank_ws], clear_canvas=True)

        # END-IF-ELSE

        return

    def evt_plot_bragg_bank(self):
        """
        Find out which bank will be plot
        Returns
        -------

        """
        # check mutex
        if self._noEventBankWidgets:
            return

        # check
        assert self._gssGroupName is not None

        # get current unit and check whether re-plot all banks is not a choice
        x_unit = str(self.ui.comboBox_xUnit.currentText())
        if x_unit != self._currBraggXUnit:
            re_plot = True
        else:
            re_plot = False
        print 'unit: %s vs. %s' % (x_unit, self._currBraggXUnit)
        self._currBraggXUnit = x_unit

        if x_unit == 'Q':
            x_unit = 'MomentumTransfer'

        # get bank IDs to plot
        plot_all_gss = self.ui.radioButton_multiGSS.isChecked()

        plot_bank_list = list()
        selected_bank_id = self.get_bragg_banks_selected()
        for bank_id in self._braggBankWidgets.keys():
            # rule out if this bank is not selected
            # no-operation for not checked
            if bank_id not in selected_bank_id:
                self._braggBankWidgetRecords[bank_id] = False
                continue

            if plot_all_gss:
                # only allow 1 check box newly checked
                print '[DB...BAT] Bank %d is previously %s.' % (bank_id, str(self._braggBankWidgetRecords[bank_id]))
                if self._braggBankWidgetRecords[bank_id]:
                    # create a mutex on bank widget check box
                    self._noEventBankWidgets = True
                    self._braggBankWidgets[bank_id].setChecked(False)
                    self._noEventBankWidgets = False

                    self._braggBankWidgetRecords[bank_id] = False
                else:
                    plot_bank_list.append(bank_id)
                    self._braggBankWidgetRecords[bank_id] = True
            else:
                # there is no limitation to plot multiple banks for 1-GSS mode
                plot_bank_list.append(bank_id)
                self._braggBankWidgetRecords[bank_id] = True
            # END-IF
        # END-FOR

        print '[DB...BAT] BraggBankWidgetRecord: ', str(self._braggBankWidgetRecords)

        # deal with the situation that there is no line to plot
        if len(plot_bank_list) == 0:
            # self.ui.graphicsView_bragg.clear_all_lines()
            self.ui.graphicsView_bragg.reset()
            return

        # check
        if plot_all_gss:
            assert len(plot_bank_list) == 1, 'Current number of banks selected is equal to %d. ' \
                                             'Must be 1.' % len(plot_bank_list)

        # determine the GSS workspace to plot
        if plot_all_gss:
            ws_group_list = self.ui.treeWidget_braggWSList.get_main_nodes()
            ws_group_list.remove('workspaces')
            print '[DB...BAT] workspace groups list:', ws_group_list
        else:
            status, ret_obj = self.ui.treeWidget_braggWSList.get_current_main_nodes()
            print '[DB...BAT] workspace group:', status, ret_obj
            if status:
                ws_group_list = ret_obj
            else:
                ws_group_list = [self._gssGroupName]
        # END-IF-ELSE

        # get the list of banks to plot or remove
        self.ui.graphicsView_bragg.reset()

        # get new bank date
        plot_data_dict = dict()
        for ws_group in ws_group_list:
            ws_data_dict = dict()
            for bank_id in plot_bank_list:
                vec_x, vec_y, vec_e = self._myController.get_bragg_data(ws_group, bank_id, x_unit)
                ws_data_dict[bank_id] = (vec_x, vec_y, vec_e)
            # END-FOR
            plot_data_dict[ws_group] = ws_data_dict
        # END-FOR

        # remove unused and plot new
        if re_plot:
            self.ui.graphicsView_bragg.reset()
            if x_unit == 'TOF':
                self.ui.graphicsView_bragg.setXYLimit(xmin=0, xmax=20000, ymin=None, ymax=None)
            elif x_unit == 'MomentumTransfer':
                self.ui.graphicsView_bragg.setXYLimit(xmin=0, xmax=20, ymin=None, ymax=None)
            elif x_unit == 'dSpacing':
                self.ui.graphicsView_bragg.setXYLimit(xmin=0, xmax=7, ymin=None, ymax=None)

        if plot_all_gss:
            self.ui.graphicsView_bragg.set_to_single_gss(False)
        else:
            self.ui.graphicsView_bragg.set_to_single_gss(True)

        self.ui.graphicsView_bragg.plot_banks(plot_data_dict, x_unit)

        return

    def evt_plot_sq(self):
        """ Event handling to plot S(Q)
        Returns
        -------

        """
        # get the raw S(Q)
        sq_name = self._myController.get_current_sq_name()

        # plot S(Q)
        self.plot_sq(sq_name, clear_prev=True)

        return

    def evt_qmax_changed(self):
        """
        Handle if the user change the value of Qmax of S(Q) including
        1. moving the right boundary in S(q) figure
        Returns:

        """
        q_min = self.ui.doubleSpinBoxQmin.value()
        q_max = self.ui.doubleSpinBoxQmax.value()

        if q_min < q_max and self.ui.graphicsView_sq.is_boundary_shown():
            self.ui.graphicsView_sq.move_right_indicator(q_max, relative=False)

        return

    def evt_qmin_changed(self):
        """

        Returns:

        """
        q_min = self.ui.doubleSpinBoxQmin.value()
        q_max = self.ui.doubleSpinBoxQmax.value()

        if q_min < q_max and self.ui.graphicsView_sq.is_boundary_shown():
            self.ui.graphicsView_sq.move_left_indicator(q_min, relative=False)

        return

    def evt_quit(self):
        """
        Quit the application
        Returns:

        """
        self.close()

    def get_default_data_dir(self):
        """
        Get default data directory
        Returns:

        """
        return self._currDataDir

    def get_workflow(self):
        """
        Return the reference to the main workflow controller
        Returns: workflow controller

        """
        return self._myController

    def process_workspace_change(self, new_ws_list):
        """
        Process (including
        1. add workspace name to tree list and etc) when detecting that
        there is some change to any workspace

        Parameters
        ----------
        new_ws_list :: list of new workspaces' names

        Returns
        -------

        """
        # check input
        assert isinstance(new_ws_list, list), 'Input workspace list must be a list of string' \
                                              'but not %s.' % str(type(new_ws_list))

        # TODO - Figure out what to do!
        # print 'current tab = ', self.ui.tabWidget_2.currentIndex(), self.ui.tabWidget_2.currentWidget(),
        # print self.ui.tabWidget_2.currentWidget().objectName()
        # print 'current workspaces: ', self._myController.get_current_workspaces()

        # add to tree
        if len(new_ws_list) > 0:
            if self.ui.tabWidget_2.currentWidget().objectName() == 'tab_gR':
                for new_ws in new_ws_list:
                    self.ui.treeWidget_grWsList.add_arb_gr(new_ws)
            elif self.ui.tabWidget_2.currentWidget().objectName() == 'tab_bragg':
                for new_ws in new_ws_list:
                    self.ui.treeWidget_braggWSList.add_arb_gr(new_ws)

        return

    def remove_gr_from_plot(self, gr_name):
        """
        Remove a GofR line from GofR canvas
        Args:
            gr_name: supposed to the G(r) name that is same as workspace name and plot key on canvas as well

        Returns:

        """
        # check
        assert isinstance(gr_name, str)

        # remove
        self.ui.graphicsView_gr.remove_gr(plot_key=gr_name)

        return

    def remove_gss_from_plot(self, gss_group_name, gss_bank_ws_name_list):
        """

        Args:
            gss_group_name: name of the GSS node, i.e., GSS workspace group's name
            gss_bank_ws_name_list: list of names of GSS single banks' workspace name

        Returns:

        """
        # check
        assert isinstance(gss_group_name, str), 'GSS group workspace name must be a string but not %s.' \
                                                '' % str(type(gss_group_name))
        assert isinstance(gss_bank_ws_name_list, list) and len(gss_bank_ws_name_list) > 0

        # get bank IDs
        bank_ids = list()
        for gss_bank_ws in gss_bank_ws_name_list:
            bank_id = int(gss_bank_ws.split('_bank')[-1])
            bank_ids.append(bank_id)

        # remove
        self.ui.graphicsView_bragg.remove_gss_banks(gss_group_name, bank_ids)

        # TODO/FIXME/ISSUE 5: check if there is no such bank's plot on figure, make sure 
        #                     the checkbox is unselected

        return

    def remove_sq_from_plot(self, sq_name):
        """
        Remove an SofQ line from SofQ canvas
        Args:
            sq_name: supposed to be the S(Q) name which is same as workspace name and plot key of canvas

        Returns:

        """
        # check
        assert isinstance(sq_name, str)

        # remove
        self.ui.graphicsView_sq.remove_sq(plot_key=sq_name)

        return

    def set_bragg_ws_to_plot(self, gss_group_name):
        """
        Set a Bragg workspace group to plot.  If the Bragg-tab is in
        (1) single-GSS mode, then switch to plot this gss_group
        (2) multiple-GSS mode, then add this group to current canvas
        Parameters
        ----------
        gss_group_name

        Returns
        -------

        """
        # check
        assert isinstance(gss_group_name, str), 'GSS workspace group name is expected to be a string, but not' \
                                                ' %s.' % str(type(gss_group_name))

        # rule out the unsupported situation
        assert gss_group_name.endswith('_group'), 'GSAS workspace group\' name must be ends with _group, ' \
                                                  'but not as %s.' % gss_group_name
        root_ws_name = gss_group_name.split('_group')[0]

        # process
        if self.ui.radioButton_multiBank.isChecked():
            # single-GSS/multi-bank mode
            # reset canvas
            self.ui.graphicsView_bragg.reset()

            # get the banks to plot
            selected_banks = self.get_bragg_banks_selected()

            bragg_ws_list = ['%s_bank%d' % (root_ws_name, bank_id) for bank_id in selected_banks]
            self.plot_bragg(bragg_ws_list=bragg_ws_list, clear_canvas=False)

        else:
            # multiple-GSS/single-bank mode
            # canvas is not be reset

            # get the bank to plot
            selected_banks = self.get_bragg_banks_selected()
            assert len(selected_banks) <= 1, 'At most 1 bank can be plot in multiple-GSS mode.'

            # form the workspace
            bragg_ws = '%s_bank%d' % (root_ws_name, selected_banks[0])

            self.plot_bragg(bragg_ws_list=[bragg_ws], clear_canvas=False)

        # END-IF-ELSE

        return

    def set_ipython_script(self, script):
        """
        Write a command (python script) to ipython console
        Parameters
        ----------
        script

        Returns
        -------

        """
        # check
        assert isinstance(script, str)

        #
        if len(script) == 0:
            # ignore
            return
        else:
            # write to the console
            self.ui.dockWidget_ipython.iPythonWidget.write_command(script)

        return

    def update_sq_boundary(self, boundary_index, new_position):
        """
        Update the S(Q) range at the main app inputs
        Returns
        -------

        """
        # check
        assert isinstance(boundary_index, int)
        assert isinstance(new_position, float)

        # set value
        if boundary_index == 1:
            # left boundary
            self.ui.doubleSpinBoxQmin.setValue(new_position)
        elif boundary_index == 2:
            # right boundary
            self.ui.doubleSpinBoxQmax.setValue(new_position)
        else:
            # exception
            raise RuntimeError('Boundary index %f in method update_sq_boundary() is not '
                               'supported.' % new_position)

        return

# step1
    def select_current_folder_clicked(self):
        o_gui = Step1GuiHandler(parent = self)
        o_gui.select_working_folder()

    def diamond_edited(self):
        self.check_step1_gui()
        
    def diamond_background_edited(self):
        self.check_step1_gui()
        
    def vanadium_edited(self):
        self.check_step1_gui()
        
    def vanadium_background_edited(self):
        self.check_step1_gui()
        
    def sample_background_edited(self):
        self.check_step1_gui()
        
    def output_folder_radio_buttons(self):
        o_gui_handler = Step1GuiHandler(parent=self)
        o_gui_handler.manual_output_folder_button_handler()
        o_gui_handler.check_go_button()

    def manual_output_folder_field_edited(self):
        self.check_step1_gui()
        
    def check_step1_gui(self):
        '''check the status of the step1 GUI in order to enable or not the GO BUTTON at the bottom'''
        o_gui_handler = Step1GuiHandler(parent=self)
        o_gui_handler.check_go_button()
        
    def run_autonom(self):
        """Will first create the output folder, then create the exp.ini file"""
        _run_autonom = RunStep1(parent = self)
        _run_autonom.create_folder()
        _run_autonom.create_exp_ini_file()

# step2
    def move_to_folder_clicked(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.move_to_folder()
        self.populate_table_clicked()
        
    def populate_table_clicked(self):
        if self.debugging:
            self.current_folder = os.getcwd()  + '/autoNOM_01/'
        else:
            self.current_folder = os.getcwd()

        _pop_table = PopulateMasterTable(parent = self)
        _pop_table.run()
        _error_reported = _pop_table.error_reported
        
        if _error_reported:
            return
        
        _pop_back_wdg = PopulateBackgroundWidgets(parent = self)
        _pop_back_wdg.run()
        
        _o_gui = Step2GuiHandler(parent = self)
        _o_gui.check_gui()

    def table_select_state_changed(self, state, row):
        _o_gui = Step2GuiHandler(parent = self)
        _o_gui.check_gui()

    def check_q_range(self):
        _o_gui = Step2GuiHandler(parent = self)
        _o_gui.check_gui()

    def check_step2_gui(self, row, column):
        _o_gui = Step2GuiHandler(parent = self)
        _o_gui.check_gui()
            
    def hidrogen_clicked(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.hidrogen_clicked()
    
    def no_hidrogen_clicked(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.no_hidrogen_clicked()
    
    def yes_background_clicked(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.yes_background_clicked()
    
    def no_background_clicked(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.no_background_clicked()
        
    def background_combobox_changed(self, index):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.background_index_changed(row_index = index)

    def reset_q_range(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.reset_q_range()

    def run_ndabs_clicked(self):
        o_create_sample_files = CreateSampleFiles(parent = self)
        o_create_sample_files.run()
        
        list_sample_files = o_create_sample_files.list_sample_files
        
        o_create_ndsum_file = CreateNdsumFile(parent = self)
        o_create_ndsum_file.run()

        o_run_ndsum = RunNDabs(parent = self, list_sample_files = list_sample_files)
        o_run_ndsum.run()
        
    def check_fourier_filter_widgets(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.check_gui()

    def check_plazcek_widgets(self):
        o_gui = Step2GuiHandler(parent = self)
        o_gui.check_gui()
        
    def table_right_click(self, position):
        _o_table = TableHandler(parent = self)
        _o_table.right_click(position = position)

    def run_sum_scans_clicked(self):
        o_run_sum_scans = RunSumScans(parent = self)
        o_run_sum_scans.run()

    # tab3 - ascii display
    def browse_ascii_file_clicked(self):
        o_gui = Step3GuiHandler(parent = self)
        o_gui.browse_file()


def main():
    app = PyQt4.QtGui.QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(PyQt4.QtGui.QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
