import os
from qtpy.QtWidgets import QFileDialog, QMessageBox

import addie.utilities.specify_plots_style as ps
import addie.calculate_gr.edit_sq_dialog


def load_sq(main_window):
    """
    Load S(Q) from file
    Returns
    -------

    """
    # get default dir
    if main_window._currDataDir is None:
        default_dir = os.getcwd()
    else:
        default_dir = getDefaultDir(main_window,
                                    sub_dir='SofQ')

    # get the file
    ext = 'nxs (*.nxs);;dat (*.dat);;All (*.*)'
    sq_file_names = QFileDialog.getOpenFileNames(main_window,
                                                 'Choose S(Q) File',
                                                 default_dir,
                                                 ext)
    if isinstance(sq_file_names, tuple):
        sq_file_names = sq_file_names[0]
    if sq_file_names is None or sq_file_names == '' or len(sq_file_names) == 0:
        return

    # update current data directory
    main_window._currDataDir = os.path.split(os.path.abspath(sq_file_names[0]))[0]
    check_in_fixed_dir_structure(main_window, 'SofQ')

    # load S(q)
    for sq_file_name in sq_file_names:
        sq_file_name = str(sq_file_name)
        sq_ws_name, q_min, q_max = main_window._myController.load_sq(sq_file_name)
        # add to color management
        color = main_window._pdfColorManager.add_sofq(sq_ws_name)

        # set to the tree and combo box
        main_window.calculategr_ui.treeWidget_grWsList.add_sq(sq_ws_name)
        main_window.calculategr_ui.comboBox_SofQ.addItem(sq_ws_name)
        main_window.calculategr_ui.comboBox_SofQ.setCurrentIndex(main_window.calculategr_ui.comboBox_SofQ.count() - 1)

        # set the UI widgets
        main_window.calculategr_ui.doubleSpinBoxQmin.setValue(q_min)
        main_window.calculategr_ui.doubleSpinBoxQmax.setValue(q_max)

        # plot S(Q) - TODO why is it getting the name again?
        ws_name = main_window._myController.get_current_sq_name()

        plot_sq(main_window, ws_name, color=color, clear_prev=False)

        # calculate and calculate G(R)
        generate_gr_step1(main_window)

def getDefaultDir(main_window, sub_dir):
    """ Get the default data directory.
    If is in Fixed-Directory-Structure, then _currDataDir is the parent directory for all GSAS, gofr and SofQ
    and thus return the data directory with _currDataDir joined with sub_dir
    Otherwise, no operation
    """
    # check
    assert isinstance(sub_dir, str), 'sub directory must be a string but not %s.' % type(sub_dir)

    if main_window._inFixedDirectoryStructure:
        default_dir = os.path.join(main_window._currDataDir, sub_dir)
    else:
        default_dir = main_window._currDataDir

    return default_dir

def check_in_fixed_dir_structure(main_window, sub_dir):
    """
    Check whether _currDataDir ends with 'GSAS', 'gofr' or 'SofQ'
    If it is, then reset the _currDataDir to its upper directory and set the in-format flag;
    Otherwise, keep as is
    """
    # make sure that the last character of currDataDir is not /
    if main_window._currDataDir.endswith('/') or main_window._currDataDir.endswith('\\'):
        # consider Linux and Windows case
        main_window._currDataDir = main_window._currDataDir[:-1]

    # split
    main_path, last_dir = os.path.split(main_window._currDataDir)
    if last_dir == sub_dir:
        main_window._inFixedDirectoryStructure = True
        main_window._currDataDir = main_path
    else:
        main_window._inFixedDirectoryStructure = False

def plot_sq(main_window, ws_name, color, clear_prev):
    """
    Plot S(Q)
    :param ws_name:
    :param sq_color: color of S(Q).  If None, then try to find it from PDF color manager
    :param clear_prev:
    :return:
    """
    # clear previous lines
    if clear_prev:
        main_window.calculategr_ui.graphicsView_sq.reset()

    # get data
    vec_q, vec_sq, vec_se = main_window._myController.get_sq(ws_name)

    # get color
    if not color:
        color = main_window._pdfColorManager.add_sofq(ws_name)

    # convert to the function to plot
    sq_type = str(main_window.calculategr_ui.comboBox_SofQType.currentText())
    plottable_name = main_window._myController.calculate_sqAlt(ws_name, sq_type)

    main_window.calculategr_ui.graphicsView_sq.plot_sq(plottable_name,
                                                       sq_y_label=sq_type,
                                                       reset_color_mark=clear_prev,
                                                       color=color)

def generate_gr_step1(main_window):
    """ Handling event from push button 'Generate G(r)' by generating G(r) of selected workspaces
    :return:
    """
    # get S(Q) workspace
    selected_sq = str(main_window.calculategr_ui.comboBox_SofQ.currentText())
    if selected_sq == 'All':
        sq_ws_name_list = list()
        for index in range(main_window.calculategr_ui.comboBox_SofQ.count()):
            item = str(main_window.calculategr_ui.comboBox_SofQ.itemText(index))
            if item != 'All':
                # add S(Q) name unless it is 'All'
                sq_ws_name_list.append(item)
            # END-IF
        # END-FOR
    else:
        # selected S(Q) is a single S(Q) name
        sq_ws_name_list = [selected_sq]

    # generate G(r)
    generate_gr_step2(main_window,
                      sq_ws_name_list=sq_ws_name_list)

def generate_gr_step2(main_window, sq_ws_name_list):
    """Generate G(r) from specified S(Q) workspaces
    """
    # check inputs
    assert isinstance(sq_ws_name_list, list), 'S(Q) workspaces {0} must be given by list but not {1}.' \
                                              ''.format(sq_ws_name_list, type(sq_ws_name_list))
    if len(sq_ws_name_list) == 0:
        raise RuntimeError('User specified an empty list of S(Q)')

    # get r-range and q-range
    min_r = float(main_window.calculategr_ui.doubleSpinBoxRmin.value())
    max_r = float(main_window.calculategr_ui.doubleSpinBoxRmax.value())
    delta_r = float(main_window.calculategr_ui.doubleSpinBoxDelR.value())

    min_q = float(main_window.calculategr_ui.doubleSpinBoxQmin.value())
    max_q = float(main_window.calculategr_ui.doubleSpinBoxQmax.value())

    use_filter_str = str(main_window.calculategr_ui.comboBox_pdfCorrection.currentText())
    if use_filter_str == 'No Modification':
        pdf_filter = None
    elif use_filter_str == 'Lorch':
        pdf_filter = 'lorch'
    else:
        raise RuntimeError('PDF filter {0} is not recognized.'.format(use_filter_str))
    rho0_str = str(main_window.calculategr_ui.lineEdit_rho.text())
    try:
        rho0=float(rho0_str)
    except ValueError:
        rho0 = None

    # PDF type
    pdf_type = str(main_window.calculategr_ui.comboBox_pdfType.currentText())

    # loop for all selected S(Q)
    for sq_ws_name in sq_ws_name_list:
        # calculate G(r)
        gr_ws_name = main_window._myController.calculate_gr(sq_ws_name,
                                                            pdf_type,
                                                            min_r,
                                                            delta_r,
                                                            max_r,
                                                            min_q,
                                                            max_q,
                                                            pdf_filter,
                                                            rho0)

        # check whether G(r) is on GofR plot or not in order to determine this is an update or new plot
        update = main_window.calculategr_ui.graphicsView_gr.has_gr(gr_ws_name)

        # plot G(R)
        if not update:
            # a new line
            gr_color, gr_style, gr_marker, gr_alpha = main_window._pdfColorManager.add_gofr(sq_ws_name,
                                                                                            gr_ws_name,
                                                                                            max_q)
            gr_label = '{0} Q: ({1}, {2})'.format(sq_ws_name, min_q, max_q)
            plot_gr(main_window, gr_ws_name, gr_color,
                    gr_style, gr_marker,
                    gr_alpha, gr_label)
        else:
            plot_gr(main_window, gr_ws_name, line_color=None,
                    line_style=None, line_marker=None,
                    line_alpha=None, line_label=None)

        # add to tree
        # TODO/ISSUE/NOW - Need to find out the name of the
        gr_param_str = 'G(r) for Q(%.3f, %.3f)' % (min_q, max_q)
        main_window.calculategr_ui.treeWidget_grWsList.add_gr(gr_param_str, gr_ws_name)

def evt_qmin_changed(main_window):
    q_min = main_window.calculategr_ui.doubleSpinBoxQmin.value()
    q_max = main_window.calculategr_ui.doubleSpinBoxQmax.value()

    if q_min < q_max and main_window.calculategr_ui.graphicsView_sq.is_boundary_shown():
        main_window.calculategr_ui.graphicsView_sq.move_left_indicator(q_min,
                                                                       relative=False)

def evt_qmax_changed(main_window):
    """
    Handle if the user change the value of Qmax of S(Q) including
    1. moving the right boundary in S(q) figure
    Returns:

    """
    q_min = main_window.calculategr_ui.doubleSpinBoxQmin.value()
    q_max = main_window.calculategr_ui.doubleSpinBoxQmax.value()

    if q_min < q_max and main_window.calculategr_ui.graphicsView_sq.is_boundary_shown():
        main_window.calculategr_ui.graphicsView_sq.move_right_indicator(q_max, relative=False)

    return

def plot_gr(main_window, ws_name, line_color, line_style,
            line_marker, line_alpha, line_label,
            auto=False):
    """Plot G(r) by their names (workspace as protocol)
    """
    # get the value
    vec_r, vec_g, vec_ge = main_window._myController.get_ws_data(ws_name)

    # check whether the workspace is on the figure
    print('[DB...BAT] G(r) graphic has plot {0} is {1}. Keys are {2}'
          ''.format(ws_name, main_window.calculategr_ui.graphicsView_gr.has_gr(ws_name),
                    main_window.calculategr_ui.graphicsView_gr.get_current_grs()))

    if main_window.calculategr_ui.graphicsView_gr.has_gr(ws_name):
        # update G(r) value of an existing plot
        main_window.calculategr_ui.graphicsView_gr.update_gr(ws_name, ws_name, plotError=False)
    else:
        # a new g(r) plot
        if auto:
            line_color, line_style, line_alpha = main_window._pdfColorManager.get_gr_line(ws_name)

         # plot G(R)
        main_window.calculategr_ui.graphicsView_gr.plot_gr(ws_name, ws_name, plotError=False,
                                        color=line_color, style=line_style, marker=line_marker,
                                        alpha=line_alpha, label=line_label)

def evt_change_sq_type(main_window):
    """ Event handling to plot S(Q)
    """
    # get the current S(Q) names
    curr_sq_list = main_window.calculategr_ui.graphicsView_sq.get_shown_sq_names()
    if len(curr_sq_list) == 0:
        return

    # reset the canvas
    main_window.calculategr_ui.graphicsView_sq.reset()

    # re-plot
    for sq_name in curr_sq_list:
        # plot S(Q)
        plot_sq(main_window, sq_name, color=None, clear_prev=False)

def do_rescale_sofq(main_window):
    """ Rescale the figure of S(Q)
    """
    min_y_value = main_window.calculategr_ui.graphicsView_sq.get_y_min()
    max_y_value = main_window.calculategr_ui.graphicsView_sq.get_y_max()
    delta_y = max(1, max_y_value - min_y_value)

    y_lower_limit = min_y_value - delta_y * 0.05
    y_upper_limit = max_y_value + delta_y * 0.05

    main_window.calculategr_ui.graphicsView_sq.setXYLimit(ymin=y_lower_limit, ymax=y_upper_limit)

def do_rescale_gofr(main_window):
    """ Rescale the figure of G(r)
    """
    min_y_value = main_window.calculategr_ui.graphicsView_gr.get_y_min()
    max_y_value = main_window.calculategr_ui.graphicsView_gr.get_y_max()
    delta_y = max(1, max_y_value - min_y_value)

    y_lower_limit = min_y_value - delta_y * 0.05
    y_upper_limit = max_y_value + delta_y * 0.05

    main_window.calculategr_ui.graphicsView_gr.setXYLimit(ymin=y_lower_limit, ymax=y_upper_limit)

def do_show_sq_bound(main_window):
    """
    Show or hide the left and right boundary of the S(Q)
    """
    q_left = main_window.calculategr_ui.doubleSpinBoxQmin.value()
    q_right = main_window.calculategr_ui.doubleSpinBoxQmax.value()
    main_window.calculategr_ui.graphicsView_sq.toggle_boundary(q_left, q_right)

def do_load_gr(main_window):
    """
    Load an ASCII file containing G(r)
    """
    # get default dir
    if main_window._currDataDir is None:
        default_dir = os.getcwd()
    else:
        default_dir = getDefaultDir(main_window, 'gofr')

    # pop out file
    file_filter = 'Data Files (*.dat);; PDFgui (*.gr);;All Files (*.*)'
    g_file_name = QFileDialog.getOpenFileName(main_window, 'Open a G(r) file', default_dir, file_filter)
    if isinstance(g_file_name, tuple):
        g_file_name = g_file_name[0]
    # return if operation is cancelled
    if g_file_name is None or g_file_name == '':
        return

    # update current data directory
    main_window._currDataDir = os.path.split(os.path.abspath(g_file_name))[0]
    # set default data directory if in fixed file structure
    check_in_fixed_dir_structure(main_window, 'gofr')

    # read file
    status, ret_obj = main_window._myController.load_gr(g_file_name)
    if not status:
        err_msg = ret_obj
        print('[Error]: %s' % err_msg)
        return
    else:
        gr_ws_name = ret_obj

    # plot
    gr_color, gr_style, gr_marker, gr_alpha = main_window._pdfColorManager.add_gofr(None,
                                                                                    gr_ws_name,
                                                                                    None)
    gr_label = gr_ws_name

    plot_gr(main_window, gr_ws_name,
            line_color=gr_color,
            line_style=gr_style,
            line_marker=gr_marker,
            line_alpha=gr_alpha,
            line_label=gr_label)

    # put the loaded G(r) workspace to tree 'workspaces'
    main_window.calculategr_ui.treeWidget_grWsList.add_child_main_item('workspaces', gr_ws_name)

def do_save_gr(main_window):
    """
    Save the selected the G(r) from menu to ASCII file
    """
    # TEST/ISSUE/NOW - Look at https://github.com/neutrons/FastGR/issues/28

    # read the selected item from the tree
    gr_name_list = main_window.calculategr_ui.treeWidget_grWsList.get_selected_items_of_level(2, excluded_parent='SofQ',
                                                                           return_item_text=True)
    if len(gr_name_list) != 1:
        err_msg = 'Error! Only 1 workspace of G(r) that can be selected.  So far %d is selected.' \
            'They are %s.' % (len(gr_name_list), str(gr_name_list))
        QMessageBox.warning(main_window, 'Error', err_msg)
        return
    else:
        gr_ws_name = gr_name_list[0]

    # pop-up a dialog for the file to save
    default_dir = os.getcwd()
    caption = 'Save G(r)'

    # TEST/ISSUE/NOW - Refactor the following part out to be a standard widget
    file_filter_str = 'XYE (*.xye);;CSV XYE (*.csv);;PDFgui (*.gr);;RMCProfile (*.dat)'
    gr_file_name = get_file_names_from_dialog(default_dir, file_filter_str, caption)[0]

    # check the file extension and use the file extension to determine G(r) file type
    file_name, file_ext = os.path.splitext(gr_file_name)
    if file_ext.lower().startswith('.xye'):
        gr_file_type = 'xye'
    elif file_ext.lower().startswith('.csv'):
        gr_file_type = 'csv'
    elif file_ext.lower().startswith('.gr'):
        gr_file_type = 'gr'
    elif file_ext.lower().startswith('.dat'):
        gr_file_type = 'rmcprofile'
    else:
        # unsupported
        raise RuntimeError('G(r) file with extension {0} is not supported.'.format(file_ext))

    # save!
    main_window._myController.save_ascii(gr_ws_name, gr_file_name, gr_file_type)

def do_save_sq(main_window):
    """Save the selected the G(r) from menu to ASCII file
    :return:
    """
    # TEST/ISSUE/NOW - Test!

    # read the selected item from the tree... return if nothing is selected
    sq_name_list = main_window.calculategr_ui.treeWidget_grWsList.get_selected_items_of_level(2, excluded_parent='GofR',
                                                                           return_item_text=True)
    if len(sq_name_list) == 0:
        return

    # loop the SofQ name to save
    file_filter = 'XYE (*.xye);;CSV XYE (*.csv);;SofQ (*.sq)'

    for sq_name in sq_name_list:
        # get the output file name first
        out_file_name = QFileDialog.getSaveFileName(main_window,
                                                    'Input File Name to Save S(Q) {0}'.format(sq_name),
                                                    main_window._currWorkDir, file_filter)
        if isinstance(out_file_name, tuple):
            out_file_name = out_file_name[0]
        if out_file_name is None or len(out_file_name) == 0:
            # skip if the user cancel the operation on this S(Q)
            continue

        # get the directory, file name and extension
        main_window._currWorkDir = os.path.dirname(out_file_name)
        file_name, file_ext = os.path.splitext(out_file_name)
        if file_ext.lower().startswith('.xye'):
            sq_file_type = 'xye'
        elif file_ext.lower().startswith('.csv'):
            sq_file_type = 'csv'
        elif file_ext.lower().startswith('.sq'):
            sq_file_type = 'dat'
        elif file_ext.lower().startswith('.dat'):
            sq_file_type = 'dat'
        elif len(file_ext.strip()) == 0:
            raise RuntimeError('There is no extension of file {0}. Unable to determine file type.'
                               ''.format(out_file_name))
        else:
            raise RuntimeError('File type {0} cannot be recognized.'.format(file_ext))

        # save file
        main_window._myController.save_ascii(sq_name, out_file_name, sq_file_type)

def do_edit_sq(main_window):
    """
    Launch a dialog box to edit S(Q) by shift and scaling.
    :return:
    """
    # create dialog instance if it does not exist
    if main_window._editSqDialog is None:
        main_window._editSqDialog = addie.calculate_gr.edit_sq_dialog.EditSofQDialog(main_window)

    # get current S(Q) list and add to dialog
    sq_name_list = list()
    num_sq = main_window.calculategr_ui.comboBox_SofQ.count()
    for isq in range(num_sq):
        sq_name = str(main_window.calculategr_ui.comboBox_SofQ.itemText(isq))
        sq_name_list.append(sq_name)
    # END-FOR

    main_window._editSqDialog.add_sq_by_name(sq_name_list)

    # show
    main_window._editSqDialog.show()

def do_generate_sq(main_window):
    """
    generate S(Q) from G(r) by PDFFourierTransform
    """
    # TODO/ISSUE/NOW - Need to implement!
    raise NotImplementedError('Dialog box for generating S(Q) has not been implemented yet.')
    # get setup
    min_r = float(main_window.calculategr_ui.doubleSpinBoxRmin.value())
    max_r = float(main_window.calculategr_ui.doubleSpinBoxRmax.value())
    min_q = main_window.calculategr_ui.doubleSpinBoxQmin.value()
    max_q = main_window.calculategr_ui.doubleSpinBoxQmax.value()

    # launch the dialog box
    if main_window._generateSofQDialog is None:
        main_window._generateSofQDialog = blabla

    main_window._generateSofQDialog.set_r_range(min_r, max_r)
    main_window._generateSofQDialog.set_q_range(min_q, max_q)

    main_window._generateSofQDialog.show()

def do_set_gofr_color_marker(main_window):
    """
    set the color/marker to plots on G(r) canvas
    """
    # get the line ID, color, and marker
    plot_id_label_list = main_window.calculategr_ui.graphicsView_gr.get_current_plots()

    # get the line ID, color, and marker
    plot_id_list, color, marker = ps.get_plots_color_marker(main_window,
                                                            plot_label_list=plot_id_label_list)
    if plot_id_list is None:
        # operation is cancelled by user
        pass
    else:
        # set the color and mark
        for plot_id in plot_id_list:
            main_window.calculategr_ui.graphicsView_gr.updateLine(ikey=plot_id,
                                                                  linecolor=color,
                                                                  marker=marker,
                                                                  markercolor=color)

def do_set_sq_color_marker(main_window):
    """
    set the color/marker on S(q) canvas
    """
    # get the line ID, color, and marker
    plot_id_label_list = main_window.calculategr_ui.graphicsView_sq.get_current_plots()

    # get the line ID, color, and marker
    plot_id_list, color, marker = ps.get_plots_color_marker(main_window,
                                                            plot_label_list=plot_id_label_list)
    if plot_id_list is None:
        # operation is cancelled by user
        pass
    else:
        # set the color and mark
        for plot_id in plot_id_list:
            main_window.calculategr_ui.graphicsView_sq.updateLine(ikey=plot_id,
                                                                  linecolor=color,
                                                                  marker=marker,
                                                                  markercolor=color)

# events from menu
def do_reset_gr_tab(main_window):
    """
    Reset G(r)-tab, including deleting all the G(r) and S(Q) workspaces,
    clearing the G(r) and S(Q) trees, and clearing both G(r) and S(Q) canvas
    """
    # get workspace from trees
    workspace_list = main_window.calculategr_ui.treeWidget_grWsList.get_workspaces()

    # reset the tree to initial status
    main_window.calculategr_ui.treeWidget_grWsList.reset_gr_tree()

    # delete all the workspaces
    for workspace in workspace_list:
        main_window._myController.delete_workspace(workspace)

    # clear all the canvas
    main_window.calculategr_ui.graphicsView_gr.clear_all_lines()
    main_window.calculategr_ui.graphicsView_sq.clear_all_lines()

    # clear the S(Q) combo box
    main_window.calculategr_ui.comboBox_SofQ.clear()
    main_window.calculategr_ui.comboBox_SofQ.addItem('All')

def do_reset_gsas_tab(main_window):
    """
    Reset the GSAS-tab including
    1. deleting all the GSAS workspaces
    2. clearing the GSAS tree
    3. clearing GSAS canvas
    """
    # delete all workspaces: get GSAS workspaces from tree
    gsas_group_node_list = main_window.calculategr_ui.treeWidget_braggWSList.get_main_nodes(output_str=False)
    for gsas_group_node in gsas_group_node_list:
        # skip if the workspace is 'workspaces'
        gss_node_name = str(gsas_group_node.text())
        if gss_node_name == 'workspaces':
            continue
        # get the split workspaces' names and delete
        gsas_ws_name_list = main_window.calculategr_ui.treeWidget_braggWSList.get_child_nodes(gsas_group_node, output_str=True)
        for workspace in gsas_ws_name_list:
            main_window._myController.delete_workspace(workspace)
        # END-FOR

        # guess for the main workspace and delete
        gss_main_ws = gss_node_name.split('_group')[0]
        main_window._myController.delete_workspace(gss_main_ws, no_throw=True)

    # END-FOR (gsas_group_node)

    # reset the GSAS tree
    main_window.calculategr_ui.treeWidget_braggWSList.reset_bragg_tree()

    # clear checkboxes for banks
    main_window.clear_bank_checkboxes()

    # clear the canvas
    main_window.calculategr_ui.graphicsView_bragg.reset()

def edit_sq(main_window, sq_name, scale_factor, shift):
    """Edit S(Q) in workspace with scale_factor * Y[i] + shift
    :param sq_name:
    :param scale_factor:
    :param shift:
    """
    # convert
    sq_name = str(sq_name)

    # check inputs
    assert isinstance(sq_name, str), 'S(Q) workspace name {0} must be a string but not a {1}.' \
                                     ''.format(sq_name, type(sq_name))
    assert isinstance(scale_factor, float), 'Scale factor {0} must be a float but not a {1}.' \
                                            ''.format(scale_factor, type(scale_factor))
    assert isinstance(shift, float), 'Shift {0} must be a float but not a {1}.'.format(shift, type(shift))

    # call the controller
    edit_sq_name = sq_name + '_Edit'
    main_window._myController.edit_matrix_workspace(sq_name, scale_factor, shift, edit_sq_name)
    # add new S(Q)
    main_window._pdfColorManager.add_sofq(edit_sq_name)

    color, marker = main_window.calculategr_ui.graphicsView_sq.get_plot_info(sq_name)
    print('[DB...BAT] Original SofQ {0} has color {0} marker {1}'.format(color, marker))

    # re-plot
    #vec_q, vec_s, vec_e = main_window._myController.get_sq(edit_sq_name)
    #main_window.calculategr_ui.graphicsView_sq.plot_sq(edit_sq_name, vec_q, vec_s, vec_e,
    main_window.calculategr_ui.graphicsView_sq.plot_sq(edit_sq_name,
                                                       sq_y_label=sq_name + ' In Edit',
                                                       reset_color_mark=False,
                                                       color=color, marker=marker)

    # calculate G(r) too
    generate_gr_step2(main_window, [edit_sq_name])

def get_file_names_from_dialog(default_dir, file_filter, caption):
    """
    get the file name from a dialog
    """
    # TODO/TEST/NOW - Find out what this method can get!!!
    # check input
    assert isinstance(default_dir, str), 'Default directory {0} must be a string but not a {1}.' \
                                         ''.format(default_dir, type(default_dir))
    assert isinstance(file_filter, str), 'File filter {0} must be a string but not a {1}.' \
        ''.format(file_filter, type(file_filter))

    # generate a dialog to get the file name to save G(r)
    export_dialog = QFileDialog()
    export_dialog.setWindowTitle(caption)
    export_dialog.setDirectory(default_dir)
    export_dialog.setAcceptMode(QFileDialog.AcceptSave)
    export_dialog.setNameFilter(file_filter)

    # quit if it is not accepted
    if export_dialog.exec_() != QFileDialog.Accepted:
        return None
    elif len(export_dialog.selectedFiles()) == 0:
        return None

    # get the file name from dialog
    file_name_list = list()
    for file_name in export_dialog.selectedFiles():
        file_name_list.append(str(file_name))

    return file_name_list
