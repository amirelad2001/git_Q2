import sys
from pathlib import Path
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
     QApplication,
     QDialog,
     QFileDialog,
     QHBoxLayout,
     QLabel,
     QMainWindow,
     QPushButton,
     QVBoxLayout,
     QWidget,
)


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setMinimumWidth(360)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("About this application")
        title.setObjectName("aboutTitle")
        layout.addWidget(title)

        details = QLabel(
            "Name: Your Name\n"
            "Course: Your Course\n"
            "Assignment: Q2"
        )
        details.setObjectName("aboutDetails")
        layout.addWidget(details)

        repository = QLabel(
            '<a href="https://github.com/amirelad2001/YOUR_Q2_REPO">'
            "View the public GitHub repository</a>"
        )
        repository.setOpenExternalLinks(True)
        repository.setTextInteractionFlags(Qt.TextBrowserInteraction)
        layout.addWidget(repository)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button, alignment=Qt.AlignRight)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.temperatures = []
        self.profits = []

        self.setWindowTitle("Data Plotter")
        self.resize(1000, 680)

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        header_layout = QHBoxLayout()
        title = QLabel("Data Plotter")
        title.setObjectName("mainTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.load_button = QPushButton("Load Data File")
        self.load_button.setObjectName("primaryButton")
        self.load_button.clicked.connect(self.open_file_dialog)
        header_layout.addWidget(self.load_button)

        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about_dialog)
        header_layout.addWidget(self.about_button)
        layout.addLayout(header_layout)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas, stretch=1)

        self.plot_graph()

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Data File",
            "",
            "CSV files (*.csv)",
        )
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path: str) -> None:
        self.temperatures = []
        self.profits = []

        with open(file_path, 'r') as f:
            f.readline()  # דילוג על שורת הכותרת
            for line in f:
                line = line.strip()
                parts = line.split(',')
                self.temperatures.append(float(parts[0]))
                self.profits.append(float(parts[1]))

        self.plot_graph()

    def plot_graph(self) -> None:
        self.ax.clear()
        if not self.temperatures or not self.profits:
            self.ax.plot([1, 2, 3], [1, 4, 9], marker="o")
            self.ax.set_title("Load a data file to see the plot")
            self.ax.set_xlabel("Temperature")
            self.ax.set_ylabel("Profits ($)")
            self.canvas.draw()
            return

        self.ax.scatter(self.temperatures, self.profits, s=1)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_title("Ice Cream Truck Profits vs. Temperature")
        self.ax.set_xlabel("Temperature")
        self.ax.set_ylabel("Profits ($)")
        m, b = np.polyfit(self.temperatures, self.profits, 1)
        x_vals = np.array(self.temperatures)
        self.ax.plot(x_vals, m * x_vals + b, color="red")
        self.ax.text(0.05, 0.9, f"y = {m:.2f}x + {b:.2f}", transform=self.ax.transAxes)
        self.canvas.draw()

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()


def main():
    app = QApplication(sys.argv)
    stylesheet_path = Path(__file__).resolve().with_name("style.qss")
    app.setStyleSheet(stylesheet_path.read_text(encoding="utf-8"))

    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
