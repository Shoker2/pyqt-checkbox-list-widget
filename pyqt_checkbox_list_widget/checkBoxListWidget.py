from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem
from pyqt_tooltip_list_widget import ToolTipListWidget


class CheckBoxListWidget(ToolTipListWidget):
    checkedSignal = pyqtSignal(int, Qt.CheckState)

    def __init__(self):
        super().__init__()
        self.itemChanged.connect(self.__sendCheckedSignal)

    def __sendCheckedSignal(self, item):
        r_idx = self.row(item)
        state = item.checkState()
        self.checkedSignal.emit(r_idx, state)

    def addItems(self, items) -> None:
        for item in items:
            self.addItem(item)

    def addItem(self, item, checked = True) -> None:
        if isinstance(item, str):
            item = QListWidgetItem(item)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        if checked:
            item.setCheckState(Qt.CheckState.Checked)
        else:
            item.setCheckState(Qt.CheckState.Unchecked)
        super().addItem(item)

    def toggleState(self, state):
        for i in range(self.count()):
            item = self.item(i)
            if item.checkState() != state:
                item.setCheckState(state)

    def getCheckedRows(self):
        return self.__getFlagRows(Qt.Checked)

    def getUncheckedRows(self):
        return self.__getFlagRows(Qt.Unchecked)

    def __getFlagRows(self, flag: Qt.CheckState):
        flag_lst = []
        for i in range(self.count()):
            item = self.item(i)
            if item.checkState() == flag:
                flag_lst.append(i)

        return flag_lst

    def removeCheckedRows(self):
        self.__removeFlagRows(Qt.Checked)

    def removeUncheckedRows(self):
        self.__removeFlagRows(Qt.Unchecked)

    def __removeFlagRows(self, flag):
        flag_lst = self.__getFlagRows(flag)
        flag_lst = reversed(flag_lst)
        for i in flag_lst:
            self.takeItem(i)
