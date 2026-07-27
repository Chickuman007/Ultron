import sys
import os
import threading
import subprocess
from PyQt5.QtCore import Qt, QSize
from pystray import Icon, Menu, MenuItem
from PIL import Image
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt





ai_running = False

def start_floating():
    app = QApplication(sys.argv)

    label = QLabel()
    label.setWindowFlags(
        Qt.FramelessWindowHint |
        Qt.WindowStaysOnTopHint |
        Qt.Tool
    )

    # ✅ REAL TRANSPARENCY
    label.setAttribute(Qt.WA_TranslucentBackground)

    base_dir = os.path.dirname(__file__)
    gif_path = r"D:\Cursor files\JARVIS\Project\ultron.png"

    movie = QMovie(gif_path)

    movie.start()
    label.setMovie(movie)

    # auto resize window to GIF size
    label.resize(movie.frameRect().size())

    # center screen
    screen = app.primaryScreen().geometry()
    x = (screen.width() - label.width()) // 2
    y = (screen.height() - label.height()) // 2
    label.move(x, y)

    # 🔥 drag move
    def mouseMoveEvent(event):
        label.move(event.globalPos())

    label.mouseMoveEvent = mouseMoveEvent

    label.show()

    app.exec_()



# 🔥 START AI
def start_ai(icon, item):
    global ai_running

    if ai_running:
        return

    ai_running = True

    base_dir = os.path.dirname(__file__)

    # ✅ SAME PYTHON
    subprocess.Popen([
    sys.executable,
    r"D:\Cursor files\JARVIS\Ultron.py"
        ])

    # ✅ FLOATING UI THREAD
    threading.Thread(target=start_floating, daemon=True).start()


# 🔥 EXIT
def exit_app(icon, item):
    icon.stop()
    


# 🔥 TRAY ICON
base_dir = os.path.dirname(__file__)
icon_path = r"C:\Users\HP\OneDrive\Desktop\logo.webp"

image = Image.open(icon_path)

menu = Menu(
    MenuItem("Start AI", start_ai),
    MenuItem("Exit", exit_app)
)

icon = Icon("ULTRON", image, "ULTRON Assistant", menu)

icon.run()