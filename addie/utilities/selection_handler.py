import numpy as np
import pprint


class SelectionHandler:

    right_column = -1
    left_column = -2
    top_row = -1
    bottom_row = -2

    def __init__(self, selection_range):

        if len(selection_range) == 0:
            return

        # only considering the first selection in this class
        selection_range = selection_range[0]

        self.selection_range = selection_range
        self.left_column = self.selection_range.leftColumn()
        self.right_column = self.selection_range.rightColumn()
        self.top_row = self.selection_range.topRow()
        self.bottom_row = self.selection_range.bottomRow()

    def nbr_column_selected(self):
        return (self.right_column - self.left_column) + 1

    def nbr_row_selected(self):
        return (self.top_row - self.bottom_row) + 1

    def first_column_selected(self):
        return self.left_column

    def first_row_selected(self):
        return self.top_row

    def get_list_column(self):
        return np.arange(self.left_column, self.right_column+1)

    def get_list_row(self):
        return np.arange(self.top_row, self.bottom_row+1)


class SelectionHandlerMaster:

    def __init__(self, parent=None):
        self.parent = parent
        self.table_ui = self.parent.ui.h3_table


class TransferH3TableWidgetState(SelectionHandlerMaster):

    def __init__(self, parent=None):
        SelectionHandlerMaster.__init__(self, parent=parent)

    def transfer_states(self, state=None, value=''):

        selection = self.parent.ui.h3_table.selectedRanges()
        o_selection = SelectionHandler(selection)

        # enable or disable all other selected rows (if only first column selected)
        if (o_selection.nbr_column_selected() == 1):

            range_row = o_selection.get_list_row()
            column_selected = o_selection.first_column_selected()

            # activate row widget
            if (column_selected == 0):

                # apply state to all the widgets
                for _row in range_row:
                    ui = self.table_ui.cellWidget(_row, 0).children()[1]
                    ui.blockSignals(True)
                    ui.setCheckState(state)
                    ui.blockSignals(False)

            # sample or normalization, shape, abs. corr., mult. scat. corr or inelastic corr.
            elif (column_selected in [7, 10, 11, 12, 18, 21, 22, 23]):

                for _row in range_row:
                    ui = self.table_ui.cellWidget(_row, column_selected).children()[1]
                    index = ui.findText(value)
                    # we found the text
                    if index > -1:
                        if not column_selected in [7, 18]:
                            ui.blockSignals(True)
                        ui.setCurrentIndex(index)
                        if not column_selected in [7, 18]:
                            ui.blockSignals(False)


class CellsHandler(SelectionHandlerMaster):

    def __init__(self, parent=None):
        SelectionHandlerMaster.__init__(self, parent=parent)
        selection = self.parent.ui.h3_table.selectedRanges()
        self.o_selection = SelectionHandler(selection)

    def clear(self):
        list_row = self.o_selection.get_list_row()
        list_column = self.o_selection.get_list_column()

        for _row in list_row:
            for _column in list_column:
                _item = self.table_ui.item(_row, _column)
                if _item:
                    _item.setText("")

    def copy(self):
        '''first column of copy and paste have to be identical'''
        list_row = self.o_selection.get_list_row()
        list_column = self.o_selection.get_list_column()

        nbr_row = len(list_row)
        nbr_column = len(list_column)

        row_column_items = [['' for x in np.arange(nbr_column)]
                            for y in np.arange(nbr_row)]
        for _row in np.arange(nbr_row):
            for _column in np.arange(nbr_column):
                _item = self.table_ui.item(_row, _column)
                if _item:
                    row_column_items[_row][_column] = _item.text()

        self.parent.master_table_cells_copy['temp'] = row_column_items
        self.parent.master_table_cells_copy['list_column'] = list_column

    def paste(self):

        list_column_copy = self.parent.master_table_cells_copy['list_column']

        list_row_paste= self.o_selection.get_list_row()
        list_column_paste = self.o_selection.get_list_column()

        nbr_row_paste = len(list_row_paste)
        nbr_column_paste = len(list_column_paste)

        row_columns_items_to_copy = self.parent.master_table_cells_copy['temp']
        [nbr_row_copy, nbr_column_copy] = np.shape(row_columns_items_to_copy)

        # if we don't select the same amount of columns, we stop here (and inform
        # user of issue in statusbar

        if list_column_copy[0] != list_column_paste[0]:
            self.parent.ui.statusbar.setStyleSheet("color: red")
            self.parent.ui.statusbar.showMessage("Copy and Paste first column selected do not match!",
                                                 self.parent.statusbar_display_time)
            return

        # we only clicked once cell before using PASTE
        if len(list_column_paste) == 1:

            pass

        else: # we clicked several columns before clicking PASTE

            # in this case, the COPY and PASTE number of columns have to match perfectly
            if len(list_column_copy) != len(list_column_paste):
                self.parent.ui.statusbar.setStyleSheet("color: red")
                self.parent.ui.statusbar.showMessage("Copy and Paste do not cover the same number of columns!",
                                                     self.parent.statusbar_display_time)
                return

            else:
                list_intersection = set(list_column_copy).intersection(list_column_paste)
                if len(list_intersection) != len(list_column_copy):
                    self.parent.ui.statusbar.setStyleSheet("color: red")
                    self.parent.ui.statusbar.showMessage("Copy and Paste do not cover the same columns!",
                                                         self.parent.statusbar_display_time)
                    return

        # if (nbr_row_paste == 1) and (nbr_column_paste == 1):
        #     '''copy contain from current cell'''
        #     pass
        #
        # elif (nbr_row_copy == 1) and (nbr_column_copy == 1):
        #     '''copy that cell in all the cells now selected'''
        #     pass









