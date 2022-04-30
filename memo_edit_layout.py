''' Окно для редактирования вопроса '''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QTableWidget, QListWidget, QListWidgetItem,
        QLineEdit, QFormLayout,
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QButtonGroup, QRadioButton,  
        QPushButton, QLabel, QSpinBox)
from memo_app import app 

txt_Question = QLineEdit('')
txt_Answer = QLineEdit('')
txt_Wrong1 = QLineEdit('')
txt_Wrong2 = QLineEdit('')
txt_Wrong3 = QLineEdit('')

layout_form = QFormLayout()

layout_form.addRow('Вопрос:', txt_Question)
layout_form.addRow('Правильный ответ:', txt_Answer)
layout_form.addRow('Неправильный вариант №1:', txt_Wrong1)
layout_form.addRow('Неправильный вариант №2', txt_Wrong2)
layout_form.addRow('Неправильный вариант №3:', txt_Wrong3)

