import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsItem, QVBoxLayout, QWidget, QPushButton, QComboBox
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QBrush

# Constants for UI
ICON_SIZE = 10

class PathEditor(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.path_points = []  # Store points for editing paths

    def load_path(self, data):
        """Load path data from JSON and display it"""
        self.scene.clear()
        self.path_points = []
        
        for point in data.get("path", []):
            x, y = point["x"], point["y"]
            capture_type = point.get("capture_type", "Default")
            icon = CapturePoint(x, y, capture_type)
            self.scene.addItem(icon)
            self.path_points.append(icon)
    
    def save_path(self):
        """Save current path as JSON"""
        path_data = [{"x": icon.x(), "y": icon.y(), "capture_type": icon.capture_type} for icon in self.path_points]
        return {"path": path_data}

class CapturePoint(QGraphicsEllipseItem):
    def __init__(self, x, y, capture_type):
        super().__init__(0, 0, ICON_SIZE, ICON_SIZE)
        self.setPos(x, y)
        self.setBrush(QBrush(Qt.red))
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.capture_type = capture_type

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.show_property_editor()
        super().mousePressEvent(event)

    def show_property_editor(self):
        """Show dropdown menu to edit capture type"""
        editor = CapturePointEditor(self)
        editor.show()

class CapturePointEditor(QWidget):
    def __init__(self, capture_point):
        super().__init__()
        self.capture_point = capture_point
        self.setWindowTitle("Edit Capture Point")
        self.setGeometry(100, 100, 200, 100)
        
        layout = QVBoxLayout()
        
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Default", "Image Scan", "Video Capture", "Depth Scan"])
        self.dropdown.setCurrentText(self.capture_point.capture_type)
        layout.addWidget(self.dropdown)
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_capture_type)
        layout.addWidget(save_button)
        
        self.setLayout(layout)
    
    def save_capture_type(self):
        self.capture_point.capture_type = self.dropdown.currentText()
        self.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Path Editor")
        self.setGeometry(100, 100, 800, 600)
        
        self.editor = PathEditor()
        self.setCentralWidget(self.editor)
        
        # Menu Bar
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        
        load_action = file_menu.addAction("Load Path")
        load_action.triggered.connect(self.load_path)
        
        save_action = file_menu.addAction("Save Path")
        save_action.triggered.connect(self.save_path)
    
    def load_path(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Path File", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, "r") as file:
                data = json.load(file)
                self.editor.load_path(data)
    
    def save_path(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Path File", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, "w") as file:
                json.dump(self.editor.save_path(), file, indent=4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
