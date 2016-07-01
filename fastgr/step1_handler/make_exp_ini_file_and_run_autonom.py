import os


class MakeExpIniFileAndRunAutonom(object):
    
    _dict_mandatory = None
    _dict_optional = None
    EXP_INI_FILENAME = 'exp.ini'
    _star = '*' * 19
    title_mandatory = 'required ' + _star
    _star = '*' * 18
    title_optional = 'optional ' + _star
    list_mandatory = ['Dia', 'DiaBg', 'Vana', 'VanaBg', 'MTc']
    list_optional = ['recali', 'renorm', 'autotemp', 'scan1', 'scanl', 'Hz', '#']
    script_to_run = "python ~zjn/pytest/autoNOM.py &"
    
    def __init__(self, parent=None, folder=None):
        self.parent = parent
        self.folder = folder
        
    def create(self):
        self.retrieve_metadata()
        self.create_exp_ini_file()

    def run_autonom(self):
        self.run_auto_nom_script()

    def retrieve_metadata(self):
        _dict_mandatory = {}
        _dict_optional = {}
        
        _diamond = str(self.parent.diamond.text())
        _diamond_background = str(self.parent.diamond_background.text())
        _vanadium = str(self.parent.vanadium.text())
        _vanadium_background = str(self.parent.vanadium_background.text())
        _sample_background = str(self.parent.sample_background.text())
        
        _first_scan = str(self.parent.first_scan.text())
        _last_scan = str(self.parent.last_scan.text())
        _frequency = self.parent.frequency.currentText()

        _recalibration_flag = self.yes_no(self.parent.recalibration_yes.isChecked())
        _renormalization_flag = self.yes_no(self.parent.renormalization_yes.isChecked())
        _autotemplate_flag = self.yes_no(self.parent.autotemplate_yes.isChecked())
        
        _comments = self.parent.comments.text()
        
        _dict_mandatory['Dia'] = _diamond
        _dict_mandatory['DiaBg'] = _diamond_background
        _dict_mandatory['Vana'] = _vanadium
        _dict_mandatory['VanaBg'] = _vanadium_background
        _dict_mandatory['MTc'] = _sample_background
        _dict_optional['recali'] = _recalibration_flag
        _dict_optional['renorm'] = _renormalization_flag
        _dict_optional['autotemp'] = _autotemplate_flag
        _dict_optional['scan1'] = _first_scan
        _dict_optional['scanl'] = _last_scan
        _dict_optional['Hz'] = _frequency
        _dict_optional['#'] = _comments
        
        self._dict_mandatory = _dict_mandatory
        self._dict_optional = _dict_optional
        
    def create_exp_ini_file(self):
        
        _full_file_name = os.path.join(self.folder, self.EXP_INI_FILENAME)
        
        f = open(_full_file_name, 'w') 

        # mandatory part
        _dict_mandatory = self._dict_mandatory
        f.write(self.title_mandatory + "\n")
        for _name in self.list_mandatory:
            f.write(_name + ' ' + _dict_mandatory[_name] + '\n')
    
        # optional part
        _dict_optional = self._dict_optional
        f.write(self.title_optional + '\n')
        for _name in self.list_optional:
            _value = _dict_optional[_name]
            if _value == '':
                continue
            else:
                f.write(_name + ' ' + _dict_optional[_name] + '\n')

        f.close()
        
    def run_auto_nom_script(self):
        _script_to_run = self.script_to_run
        os.chdir(self.folder)
        self.parent.current_folder_label.setText(self.folder)
        os.system(_script_to_run)
        self.parent.statusbar.showMessage("autoNOM script: DONE !")        

    def yes_no(self, condition):
        if condition:
            return "yes"
        else:
            return "no"