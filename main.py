import sys
from pathlib import Path
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPixmap
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
        self.setWindowTitle("About Me")
        self.setMinimumWidth(520)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        image_path = Path(__file__).resolve().with_name("bob.jpg")
        image = QPixmap(str(image_path))
        if image.isNull():
            raise FileNotFoundError(f"Could not load the About picture: {image_path}")

        picture = QLabel()
        picture.setAccessibleName("Amir Elad's picture")
        picture.setAlignment(Qt.AlignmentFlag.AlignCenter)
        picture.setPixmap(
            image.scaled(
                190,
                190,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        layout.addWidget(picture, alignment=Qt.AlignmentFlag.AlignTop)

        details_layout = QVBoxLayout()
        details_layout.setSpacing(10)

        title = QLabel("Amir Elad")
        title.setObjectName("aboutTitle")
        details_layout.addWidget(title)

        details = QLabel(
            "Email: 123amire@gmail.com\n"
            "Course: practical programming\n"
            "Assignment: Q2"
        )
        details.setObjectName("aboutDetails")
        details_layout.addWidget(details)

        linkedin = QLabel(
            '<a href="https://www.linkedin.com/in/amir-elad-bbbb853b4/">'
            "LinkedIn profile</a>"
        )
        linkedin.setOpenExternalLinks(True)
        linkedin.setTextInteractionFlags(Qt.TextBrowserInteraction)
        details_layout.addWidget(linkedin)

        repository = QLabel(
            '<a href="https://github.com/amirelad2001/git_Q2">'
            "Public GitHub repository</a>"
        )
        repository.setOpenExternalLinks(True)
        repository.setTextInteractionFlags(Qt.TextBrowserInteraction)
        details_layout.addWidget(repository)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        details_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)
        details_layout.addStretch()
        layout.addLayout(details_layout)


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
        self.figure.set_facecolor("white")
        self.ax.set_facecolor("white")
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.set_toolbar_icons_black()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas, stretch=1)

        self.plot_graph()

    def set_toolbar_icons_black(self) -> None:
        for action in self.toolbar.actions():
            if action.isSeparator():
                continue

            pixmap = action.icon().pixmap(
                self.toolbar.iconSize(),
                QIcon.Mode.Normal,
                QIcon.State.Off,
            )
            if pixmap.isNull():
                continue

            image = pixmap.toImage()
            for y in range(image.height()):
                for x in range(image.width()):
                    pixel = image.pixelColor(x, y)
                    if pixel.alpha():
                        image.setPixelColor(x, y, QColor(0, 0, 0, pixel.alpha()))

            black_pixmap = QPixmap.fromImage(image)
            black_icon = QIcon()
            for mode in (
                QIcon.Mode.Normal,
                QIcon.Mode.Disabled,
                QIcon.Mode.Active,
                QIcon.Mode.Selected,
            ):
                for state in (QIcon.State.Off, QIcon.State.On):
                    black_icon.addPixmap(black_pixmap, mode, state)
            action.setIcon(black_icon)

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
            f.readline()   
            for line in f:
                line = line.strip()
                parts = line.split(',')
                self.temperatures.append(float(parts[0]))
                self.profits.append(float(parts[1]))

        self.plot_graph()

    def plot_graph(self) -> None:
        self.ax.clear()
        self.figure.set_facecolor("white")
        self.ax.set_facecolor("white")
        self.ax.tick_params(axis="both", colors="black")
        for spine in self.ax.spines.values():
            spine.set_color("black")
            spine.set_visible(True)

        if not self.temperatures or not self.profits:
            self.ax.plot(
                [1, 2, 3],
                [1, 4, 9],
                color="black",
                marker="o",
                markerfacecolor="black",
                markeredgecolor="black",
            )
            self.ax.set_title("Load a data file to see the plot", color="black")
            self.ax.set_xlabel("Temperature", color="black")
            self.ax.set_ylabel("Profits ($)", color="black")
            self.canvas.draw()
            return

        self.ax.scatter(self.temperatures, self.profits, s=1, color="black")
        self.ax.set_title("Ice Cream Truck Profits vs. Temperature", color="black")
        self.ax.set_xlabel("Temperature", color="black")
        self.ax.set_ylabel("Profits ($)", color="black")
        m, b = np.polyfit(self.temperatures, self.profits, 1)
        x_vals = np.array(self.temperatures)
        self.ax.plot(x_vals, m * x_vals + b, color="black")
        self.ax.text(
            0.05,
            0.9,
            f"y = {m:.2f}x + {b:.2f}",
            color="black",
            transform=self.ax.transAxes,
        )
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
