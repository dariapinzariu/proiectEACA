import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt


class CubicEquationSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ecuatia de gradul al treilea')
        self.setGeometry(100, 100, 800, 600)

        # Adăugăm un fundal
        self.setAutoFillBackground(True)
        p = self.palette()
        bg_image = QPixmap("background.jpg")  # imaginea de fundal
        p.setBrush(QPalette.Window, QBrush(bg_image))
        self.setPalette(p)

        # Layout principal
        main_layout = QVBoxLayout()

        # Titlu
        title_label = QLabel("Calculator Ecuatie de Gradul 3")
        title_label.setStyleSheet("color: pink; font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Layout pentru introducerea coeficienților
        coef_layout = QVBoxLayout()
        coef_layout.setSpacing(10)

        self.label_a = QLabel('Coeficient a:')
        self.entry_a = QLineEdit()
        self.label_b = QLabel('Coeficient b:')
        self.entry_b = QLineEdit()
        self.label_c = QLabel('Coeficient c:')
        self.entry_c = QLineEdit()
        self.label_d = QLabel('Coeficient d:')
        self.entry_d = QLineEdit()

        for label, entry in [(self.label_a, self.entry_a), (self.label_b, self.entry_b),
                             (self.label_c, self.entry_c), (self.label_d, self.entry_d)]:
            label.setStyleSheet("color: pink; font-size: 16px;")
            entry.setStyleSheet("background-color: white;")
            coef_layout.addWidget(label)
            coef_layout.addWidget(entry)

        # Layout pentru butoane și afișare soluții
        button_layout = QHBoxLayout()

        self.solve_button = QPushButton('Calculează soluțiile')
        self.solve_button.clicked.connect(self.solve_and_display)
        self.plot_button = QPushButton('Desenează graficul')
        self.plot_button.clicked.connect(self.plot_cubic_graph)

        for button in [self.solve_button, self.plot_button]:
            button.setStyleSheet("background-color: pink; color: white; font-size: 16px;")
            button_layout.addWidget(button)

        # Layout pentru soluții și grafic
        solutions_and_plot_layout = QVBoxLayout()

        # Label pentru afișarea soluțiilor
        self.solution_label = QLabel("Ecuatia a*x^3 + b*x^2 + c*x + d = 0 are solutiile:")
        self.solution_label.setStyleSheet("color: pink; font-size: 16px;")
        self.solutions_display = QLabel("x1 = \nx2 = \nx3 = ")
        self.solutions_display.setStyleSheet("color: white; font-size: 16px;")

        # Adăugăm graficul
        self.graph_display = QLabel()
        self.graph_display.setAlignment(Qt.AlignCenter)

        # Adaugă elementele în layout-ul pentru soluții și grafic
        solutions_and_plot_layout.addWidget(self.solution_label)
        solutions_and_plot_layout.addWidget(self.solutions_display)
        solutions_and_plot_layout.addWidget(self.graph_display)

        # Adaugă layout-urile la layout-ul principal
        main_layout.addLayout(coef_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(solutions_and_plot_layout)

        self.setLayout(main_layout)

    def solve_cubic(self, a, b, c, d):
        # Utilizăm metoda numpy.roots pentru a găsi toate rădăcinile (inclusiv cele complexe)
        coefficients = [a, b, c, d]
        roots = np.roots(coefficients)
        return roots

    def solve_and_display(self):
        try:
            a = float(self.entry_a.text())
            b = float(self.entry_b.text())
            c = float(self.entry_c.text())
            d = float(self.entry_d.text())

            if a == 0:
                QMessageBox.critical(self, "Error",
                                     "Coeficientul a trebuie să fie diferit de zero pentru o ecuație de gradul 3.")
                return

            solutions = self.solve_cubic(a, b, c, d)
            solution_text = ""
            for i, sol in enumerate(solutions):
                if np.isclose(sol.imag, 0):
                    solution_text += f"x{i + 1} = {sol.real:.5f}\n"
                else:
                    solution_text += f"x{i + 1} = {sol.real:.5f} + {sol.imag:.5f}i\n"
            self.solutions_display.setText(solution_text)
        except ValueError:
            QMessageBox.critical(self, "Error", "Te rog să introduci valori numerice valide.")

    def plot_cubic_graph(self):
        try:
            a = float(self.entry_a.text())
            b = float(self.entry_b.text())
            c = float(self.entry_c.text())
            d = float(self.entry_d.text())

            x = np.linspace(-10, 10, 400)
            y = a * x ** 3 + b * x ** 2 + c * x + d

            plt.figure(figsize=(6, 4))
            plt.plot(x, y, color='pink')
            plt.axhline(0, color='black', linewidth=0.5)
            plt.axvline(0, color='black', linewidth=0.5)
            plt.grid(True)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.tight_layout()

            # Salvăm graficul într-un fișier temporar pentru a-l afișa în PyQt5
            temp_file = 'temp_plot.png'
            plt.savefig(temp_file)

            # Încărcăm imaginea în QLabel
            pixmap = QPixmap(temp_file)
            self.graph_display.setPixmap(pixmap)

            plt.close()  # Închidem figura pentru a elibera resursele
        except ValueError:
            QMessageBox.critical(self, "Error", "Te rog să introduci valori numerice valide.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    solver = CubicEquationSolver()
    solver.show()
    sys.exit(app.exec_())
