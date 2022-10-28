from PIL import Image
from PySide6.QtCore import QPoint, QThreadPool
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMenu, QSystemTrayIcon, QStyle
from pynput.keyboard import Key, KeyCode
from pytesseract import pytesseract

from frame import Frame
from key_listener import KeyPressListener


TESSERACT_CMD = r"D:\Programs\Tesseract-ORC\tesseract.exe"
SHORTCUT_KEY = {Key.cmd, KeyCode.from_char("z")}


class SSCopy(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFixedSize(self.size())
        self._frame = Frame(self)
        self._frame.setFixedSize(self.size())
        self._frame.captured.connect(self.captured)

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addWidget(self._frame)
        self.setLayout(self._layout)

    def captured(self, start: QPoint, end: QPoint):
        self.showMinimized()
        x, y = start.x(), start.y()
        w, h = end.x() - start.x(), end.y() - start.y()
        screenshot = self.screen().grabWindow(0, x, y, w, h)

        pytesseract.tesseract_cmd = TESSERACT_CMD

        image = Image.fromqpixmap(screenshot)
        text: str = pytesseract.image_to_string(image, lang="eng")

        clipboard = QApplication.clipboard()
        clipboard.setText(text)


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        menu = QMenu()
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.quit)
        self.setContextMenu(menu)


class Application(QWidget):

    def __init__(self):
        super().__init__()
        self.sscopy: SSCopy | None = None
        self.keypress_listener = KeyPressListener(key=SHORTCUT_KEY)
        self.keypress_listener.signal.triggered.connect(self.capture)
        QThreadPool.globalInstance().start(self.keypress_listener)

        placeholder_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DialogNoButton)
        tray_icon = SystemTrayIcon(placeholder_icon, self)
        tray_icon.show()

    def capture(self):
        self.sscopy = SSCopy()
        self.sscopy.show()

    def closeEvent(self, event) -> None:
        self.keypress_listener.stop()
        super(Application, self).closeEvent(event)


if __name__ == "__main__":
    app = QApplication()
    window = Application()
    window.hide()
    app.exec()
