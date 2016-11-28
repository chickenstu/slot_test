from PySide.QtGui import *
from PySide.QtCore import *
import sys

class PaletteListModel(QAbstractListModel):
	def __init__(self, colors=[]):
		super(PaletteListModel, self).__init__()
		#QAbstractListModel.__init__(self, parent)
		self._colors = colors

	def data(self, index, role):

		# define text itself
		if role == Qt.DisplayRole:
			row = index.row()
			color = self._colors[row]
			return color.name()
		# define icons
		elif role == Qt.DecorationRole:
			row = index.row()
			color = self._colors[row]
			pixmap = QPixmap(100, 100)
			pixmap.fill(color)
			icon = QIcon(pixmap)
			return icon
		# define tool tips
		elif role == Qt.ToolTipRole:
			row = index.row()
			color = self._colors[row]
			return color.name() + " muschi"
		# define text color
		elif role == Qt.ForegroundRole:
			return QColor("green")
		# If text is being edited, return specific string
		elif role == Qt.EditRole:
			return self._colors[index.row()].name()
		return None

	def rowCount(self, parent):
		return len(self._colors)

	def columnCount(self, parent):
		return 5

	def headerData(self, section, orientation, role):
		if role == Qt.DisplayRole:
			if orientation == Qt.Horizontal:
				return "Palette"
			else:
				return "Color {}".format(section)

	def flags(self, index):
		return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

	def setData(self, index, value, role=Qt.EditRole):
		if role == Qt.EditRole:
			row = index.row()
			color = QColor(value)
			if color.isValid():
				self._colors[row] = color
				# So all the other widgets that uses this model update right away!
				self.dataChanged.emit(index, index)
				return True
			else:
				return False



if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setStyle("CleanLooks")

	red = QColor(255,0,0)
	green = QColor(0, 255, 0)
	blue = QColor(0, 0, 255)
	model = PaletteListModel([red, green, blue])	

	combo = QComboBox()
	listv = QListView()
	tree = QTreeView()
	table = QTableView()

	combo.setModel(model)
	listv.setModel(model)
	tree.setModel(model)
	table.setModel(model)
	#combo.show()
	#listv.show()
	tree.show()
	table.show()

	sys.exit(app.exec_())
