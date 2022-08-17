from PyQt6.QtWidgets import (
    QApplication, 
    # QMainWindow,
    QWidget,
    QVBoxLayout, 
    QMessageBox,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLCDNumber,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
)

def open_alert():
    alert = QMessageBox()
    alert.setText('You clicked the button!')
    alert.exec()

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

widgets = [
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLCDNumber,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
]

for widget in widgets:
    layout.addWidget(widget())

window.setLayout(layout)
window.show()
# button = QPushButton('Click')
# button.clicked.connect(open_alert)
# button.show()

app.exec()