t=QToolBar('Redistricting')

#interactive_redistrict_tool_button = QToolButton()
#interactive_redistrict_tool_button.setAutoRaise(True)
#interactive_redistrict_tool_button.setToolTip('Interactive Redistrict')
#interactive_redistrict_tool_button.setIcon(QIcon('/home/nyall/dev/redistricting/images/interactive_redistrict.svg'))
#interactive_redistrict_tool_button.setPopupMode(QToolButton.InstantPopup)

#interactive_menu = QMenu()
general_electorate_action = QAction(QIcon('/home/nyall/dev/redistricting/images/interactive_redistrict.svg'), 'Interactive Redistrict')
#interactive_menu.addAction(general_electorate_action)
#maori_electorate_action = QAction('Maori Electorate')
#interactive_menu.addAction(maori_electorate_action)

#interactive_redistrict_tool_button.setMenu(interactive_menu)
#t.addWidget(interactive_redistrict_tool_button)
t.addAction(general_electorate_action)

#redistrict_selected_tool_button = QToolButton()
#redistrict_selected_tool_button.setAutoRaise(True)
#redistrict_selected_tool_button.setToolTip('Redistrict Selected Mesh Blocks')
#redistrict_selected_tool_button.setIcon(QIcon('/home/nyall/dev/redistricting/images/redistrict_selected.svg'))
#redistrict_selected_tool_button.setPopupMode(QToolButton.InstantPopup)

def select_new_electorate():
    dlg = ElectorateSelectionDialog(iface.mainWindow())
    dlg.exec_()

redistrict_selected_action = QAction(QIcon('/home/nyall/dev/redistricting/images/redistrict_selected.svg'),'Redistrict Selected Mesh Blocks')
redistrict_selected_action.triggered.connect(select_new_electorate)

#selected_menu = QMenu()
#selected_general_electorate_action = QAction('Assign General Electorate for Selected Meshblocks...')
#selected_general_electorate_action.triggered.connect(select_new_electorate)
#selected_menu.addAction(selected_general_electorate_action)
#selected_maori_electorate_action = QAction('Assign Maori Electorate for Selected Meshblocks...')
#selected_maori_electorate_action.triggered.connect(select_new_electorate)
#selected_menu.addAction(selected_maori_electorate_action)


#redistrict_selected_tool_button.setMenu(selected_menu)
#t.addWidget(redistrict_selected_tool_button)
t.addAction(redistrict_selected_action)

stats_tool_action=QAction(QIcon('/home/nyall/dev/redistricting/images/stats_tool.svg'),'Electorate Statistics')
t.addAction(stats_tool_action)

themes_tool_button = QToolButton()
themes_tool_button.setAutoRaise(True)
themes_tool_button.setToolTip('Map Themes')
themes_tool_button.setIcon(QIcon('/home/nyall/dev/redistricting/images/themes.svg'))
themes_tool_button.setPopupMode(QToolButton.InstantPopup)

themes_menu = QMenu()
general_theme_action = QAction('Electorates')
themes_menu.addAction(general_theme_action)
general_change_action = QAction('Electorate Changes')
themes_menu.addAction(general_change_action)
general_invalid_action = QAction('Invalid Electorates')
themes_menu.addAction(general_invalid_action)

#themes_menu.addSeparator()
#maori_theme_action = QAction('Maori Electorates')
#themes_menu.addAction(maori_theme_action)
#maori_change_action = QAction('Maori Electorate Changes')
#themes_menu.addAction(maori_change_action)
#maori_invalid_action = QAction('Maori Electorate Invalid Districts')
#themes_menu.addAction(maori_invalid_action)

themes_tool_button.setMenu(themes_menu)
t.addWidget(themes_tool_button)

new_map_themes_tool_button = QToolButton()
new_map_themes_tool_button.setAutoRaise(True)
new_map_themes_tool_button.setToolTip('New Themed Map View')
new_map_themes_tool_button.setIcon(QIcon('/home/nyall/dev/redistricting/images/new_themed_map.svg'))
new_map_themes_tool_button.setPopupMode(QToolButton.InstantPopup)

new_map_theme_menu = QMenu()
for a in themes_menu.actions():
    new_map_theme_menu.addAction(a)
new_map_themes_tool_button.setMenu(new_map_theme_menu)
t.addWidget(new_map_themes_tool_button)

switch_tool_button = QToolButton()
switch_tool_button.setAutoRaise(True)
switch_tool_button.setToolTip('Switch Task')
switch_tool_button.setIcon(QIcon('/home/nyall/dev/redistricting/images/switch_task.svg'))
switch_tool_button.setPopupMode(QToolButton.InstantPopup)
switch_menu = QMenu()
switch_ni_general_electorate_action = QAction('NI General Electorate')
switch_menu.addAction(switch_ni_general_electorate_action)
switch_si_general_electorate_action = QAction('SI General Electorate')
switch_menu.addAction(switch_si_general_electorate_action)
switch_maori_electorate_action = QAction('Māori Electorate')
switch_menu.addAction(switch_maori_electorate_action)

switch_tool_button.setMenu(switch_menu)
t.addWidget(switch_tool_button)


iface.addToolBar(t)

p = iface.mapCanvas().mapToGlobal(QtCore.QPoint(0, 0))
t.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

t.move(p.x() + 30, p.y() + 50)
t.adjustSize()

t.show()


class ElectorateSelectionDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle('Select New Electorate')
        
        l = QVBoxLayout()
        
        l.addWidget(QLabel('Recently used electorates'))
        recent_list = QListWidget()
        recent_list.setMaximumHeight(100)
        for i in range(5):
            recent_list.addItem( 'Electorate {}'.format(i))
        l.addWidget(recent_list,0)
        
        l.addWidget(QLabel('Available electorates'))
        search = QgsFilterLineEdit()
        search.setShowSearchIcon(True)
        search.setPlaceholderText('Search for electorate')
        l.addWidget(search)
        
        list = QListWidget()
        for i in range(10):
            list.addItem( 'Electorate {}'.format(i))
            
        l.addWidget(list,10)
        
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        l.addWidget(bb)
        bb.rejected.connect(self.reject)
        bb.accepted.connect(self.accept)
        
        bb.addButton("Select from Map", QDialogButtonBox.ActionRole)
            
        self.setLayout(l)
        
        

