import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QGroupBox
from PyQt5.QtGui import QPalette, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotCanvas(FigureCanvas):
    def _init_(self, parent=None):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super()._init_(self.fig)
        self.setParent(parent)
        self.plot(np.array([0]), np.array([0]))  # Initialize canvas with an empty plot

    def plot(self, x, y, color='blue'):
        self.ax.clear()
        self.ax.plot(x, y, color=color)
        self.ax.set_aspect('equal')
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Adaugă mai multe valori pe axa x și y
        self.ax.set_xticks(np.arange(-10, 11, 2))  # Extinde limitele de la -10 la 10 cu pași de 2
        self.ax.set_yticks(np.arange(-10, 11, 2))

        self.draw()

    def save_figure(self, filename):
        self.fig.savefig(filename)

    def set_dynamic_limits(self, x, y):
        margin = 1
        x_min, x_max = np.min(x) - margin, np.max(x) + margin
        y_min, y_max = np.min(y) - margin, np.max(y) + margin
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)
        self.ax.set_xticks(np.arange(np.floor(x_min), np.ceil(x_max) + 1, 2))
        self.ax.set_yticks(np.arange(np.floor(y_min), np.ceil(y_max) + 1, 2))


class TransformApp(QWidget):
    def _init_(self):
        super()._init_()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Transformări')

        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#f0f0f0'))
        self.setPalette(palette)

        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Grup pentru selecția figurilor
        figures_group = QGroupBox("Figuri")
        figures_group.setStyleSheet("QGroupBox { background-color: #e6f7ff; font: bold; }")
        figures_layout = QGridLayout()
        figures_group.setLayout(figures_layout)

        self.figures_buttons = {
            'Patrat': QPushButton('Patrat'),
            'Cerc': QPushButton('Cerc'),
            'Triunghi': QPushButton('Triunghi'),
            'Dreptunghi': QPushButton('Dreptunghi'),
            'Romb': QPushButton('Romb'),
            'Trapez': QPushButton('Trapez'),
            'Hexagon': QPushButton('Hexagon'),
            'Segment': QPushButton('Segment'),
            'Pentagon': QPushButton('Pentagon')
        }

        positions = [(i, j) for i in range(4) for j in range(3)]
        for position, name in zip(positions, self.figures_buttons.keys()):
            button = self.figures_buttons[name]
            button.setStyleSheet(
                "QPushButton { background-color: #80d4ff; font: bold; } QPushButton:hover { background-color: #b3e6ff; }")
            button.clicked.connect(self.draw_figure)
            figures_layout.addWidget(button, *position)

        # Layout pentru transformări
        transforms_group = QGroupBox("Transformări")
        transforms_group.setStyleSheet("QGroupBox { background-color: #fff0f0; font: bold; }")
        transforms_layout = QGridLayout()
        transforms_group.setLayout(transforms_layout)

        self.translate_label = QLabel('Translație, T = ')
        self.translate_entry = QLineEdit()
        self.translate_entry.setStyleSheet("QLineEdit { background-color: #ffe6e6; }")
        self.scale_label = QLabel('Omotetie, H = ')
        self.scale_entry = QLineEdit()
        self.scale_entry.setStyleSheet("QLineEdit { background-color: #ffe6e6; }")
        self.rotate_label = QLabel('Rotație, R = ')
        self.rotate_entry = QLineEdit()
        self.rotate_entry.setStyleSheet("QLineEdit { background-color: #ffe6e6; }")
        self.apply_button = QPushButton('Aplică Transformarea')
        self.apply_button.setStyleSheet(
            "QPushButton { background-color: #ff8080; font: bold; } QPushButton:hover { background-color: #ffb3b3; }")
        self.apply_button.clicked.connect(self.apply_transformation)

        self.save_button = QPushButton('Salvează Imaginea')
        self.save_button.setStyleSheet(
            "QPushButton { background-color: #80ff80; font: bold; } QPushButton:hover { background-color: #b3ffb3; }")
        self.save_button.clicked.connect(self.save_image)

        transforms_layout.addWidget(self.translate_label, 0, 0)
        transforms_layout.addWidget(self.translate_entry, 0, 1)
        transforms_layout.addWidget(self.scale_label, 1, 0)
        transforms_layout.addWidget(self.scale_entry, 1, 1)
        transforms_layout.addWidget(self.rotate_label, 2, 0)
        transforms_layout.addWidget(self.rotate_entry, 2, 1)
        transforms_layout.addWidget(self.apply_button, 3, 0, 1, 2)
        transforms_layout.addWidget(self.save_button, 4, 0, 1, 2)

        # Zona pentru grafice
        self.figure_canvas = PlotCanvas(self)
        self.transformed_canvas = PlotCanvas(self)

        # Adăugarea grupurilor și graficelor în layout-ul principal
        main_layout.addWidget(figures_group)
        main_layout.addWidget(transforms_group)
        main_layout.addWidget(self.figure_canvas)
        main_layout.addWidget(self.transformed_canvas)

    def draw_figure(self):
        sender = self.sender()
        figure_name = sender.text()

        if figure_name == 'Patrat':
            x, y = [0, 2, 2, 0, 0], [0, 0, 2, 2, 0]
        elif figure_name == 'Cerc':
            angles = np.linspace(0, 2 * np.pi, 100)
            x, y = 2 * np.cos(angles), 2 * np.sin(angles)
        elif figure_name == 'Triunghi':
            x, y = [0, 2, 1, 0], [0, 0, np.sqrt(3), 0]
        elif figure_name == 'Dreptunghi':
            x, y = [0, 4, 4, 0, 0], [0, 0, 2, 2, 0]
        elif figure_name == 'Romb':
            x, y = [0, 2, 0, -2, 0], [2, 0, -2, 0, 2]
        elif figure_name == 'Trapez':
            x, y = [0, 2, 3, -1, 0], [0, 0, 2, 2, 0]
        elif figure_name == 'Hexagon':
            angles = np.linspace(0, 2 * np.pi, 7)
            x, y = 2 * np.cos(angles), 2 * np.sin(angles)
        elif figure_name == 'Segment':
            x, y = [0, 3], [0, 3]
        elif figure_name == 'Pentagon':
            angles = np.linspace(0, 2 * np.pi, 6)
            x, y = 2 * np.cos(angles), 2 * np.sin(angles)

        self.figure_x, self.figure_y = x, y
        self.figure_canvas.plot(x, y)

    def apply_transformation(self):
        try:
            T = complex(self.translate_entry.text().strip() or "0")
            H = float(self.scale_entry.text().strip() or "1")
            R = float(self.rotate_entry.text().strip() or "0")

            z = np.array(self.figure_x) + 1j * np.array(self.figure_y)

            # Aplicați translația, omotetia și rotația
            w = H * np.exp(1j * R) * z + T

            # Actualizați limitele axelor pentru canvasul transformărilor
            self.transformed_canvas.set_dynamic_limits(w.real, w.imag)

            self.transformed_canvas.plot(w.real, w.imag, color='red')
        except Exception as e:
            print(f"Eroare la aplicarea transformării: {e}")

    def save_image(self):
        try:
            filename = 'transformed_figure.png'
            self.transformed_canvas.save_figure(filename)
            print(f"Imaginea a fost salvată ca {filename}")
        except Exception as e:
            print(f"Eroare la salvarea imaginii: {e}")


if _name_ == '_main_':
    app = QApplication(sys.argv)
    ex = TransformApp()
    ex.show()
    sys.exit(app.exec_())
