from pydm.widgets import PyDMLineEdit, PyDMLabel
from qtpy.QtCore import Property, Qt
from qtpy.QtWidgets import QGridLayout
from pydm.widgets.base import refresh_style

class PyRogueLineEdit(PyDMLineEdit):
    def __init__(self, parent, init_channel=None):
        super().__init__(parent, init_channel=init_channel)                

        self._unitWidget = PyDMLabel(parent)
        self._unitWidget.setStyleSheet("QLabel { color : DimGrey; }")
        self._unitWidget.setAlignment(Qt.AlignRight)
        self._unitWidget.setText("")

        grid = QGridLayout()
        grid.addWidget(self._unitWidget, 0, 0)
        grid.setVerticalSpacing(0)
        grid.setHorizontalSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(grid)

        self.textEdited.connect(self.text_edited)
        self._dirty = False

        self.setStyleSheet("*[dirty='true']\
                           {background-color: orange;}")

    def text_edited(self):
        self._dirty = True
        refresh_style(self)

    def focusOutEvent(self, event):
        self._dirty = False
        super(PyRogueLineEdit, self).focusOutEvent(event)
        refresh_style(self)

    @Property(bool)
    def dirty(self):
        return self._dirty

    def unit_changed(self, new_unit):
        self._unitWidget.setText(new_unit)

        
