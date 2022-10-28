from PySide6.QtCore import QObject, Signal, QRunnable
from pynput.keyboard import Key, KeyCode, Listener


class KeyPressSignal(QObject):
    triggered = Signal()


class KeyPressListener(QRunnable):
    def __init__(self, key: set[Key | KeyCode] | Key | KeyCode):
        super().__init__()
        self.current = set()
        self.signal = KeyPressSignal()
        self.listener = Listener(on_release=self.on_release)
        self.COMBINATION = key

    def on_release(self, key):
        if key in self.COMBINATION:
            self.current.add(key)
            if all(k in self.current for k in self.COMBINATION):
                self.signal.triggered.emit()
                self.current = set()

    def stop(self):
        self.listener.stop()

    def run(self) -> None:
        self.listener.start()
