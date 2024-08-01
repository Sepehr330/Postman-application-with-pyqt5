import sys
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication, QWidget

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('PyQt QTreeWidget')
        self.setGeometry(500, 400, 400, 200)
 

        tree = QTreeWidget(self)
        tree.setHeaderLabels(['History'])
        tree_widget_item1 = QTreeWidgetItem(["Today"])
        tree_widget_item1.addChild(QTreeWidgetItem(["get"]))
        tree_widget_item2 = QTreeWidgetItem(["Yesterday"])
        tree_widget_item2.addChild(QTreeWidgetItem(["push"]))
        tree_widget_item3 = QTreeWidgetItem(["Last Month"])
        tree_widget_item3.addChild(QTreeWidgetItem(["push"]))
        tree.addTopLevelItem(tree_widget_item1)
        tree.addTopLevelItem(tree_widget_item2)
        tree.addTopLevelItem(tree_widget_item3)
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())