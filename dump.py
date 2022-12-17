import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QRubberBand, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # # Set the window properties
        self.setWindowTitle('Capture Region')
        self.setGeometry(100, 100, 800, 600)

        # Create a label to display the screenshot
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)
        self.screenshot = self.grab()
        # Create the rubber band
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)

        # Connect the mouse events
        self.label.mousePressEvent = self.mouse_press_event
        self.label.mouseMoveEvent = self.mouse_move_event
        self.label.mouseReleaseEvent = self.mouse_release_event

    def mouse_press_event(self, event):
        # Save the mouse press position
        self.origin = event.pos()

        # Show the rubber band
        self.rubber_band.setGeometry(QRect(self.origin, event.pos()))
        self.rubber_band.show()

    def mouse_move_event(self, event):
        # Update the rubber band size
        self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouse_release_event(self, event):
        # Hide the rubber band
        self.rubber_band.hide()

        # Capture the selected region of the screen
        region = QRect(self.origin, event.pos())
        image = self.screenshot.copy(region)

        # Save the image to a file
        image.save('screenshot.png')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
