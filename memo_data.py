from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from random import randint, shuffle

new_quest_templ = 'Новый вопрос' # такая строка будет устанавливаться по умолчанию для новых вопросов
new_answer_templ = 'Новый ответ' # то же для ответов

text_wrong = 'Неверно'
text_correct = 'Верно'

class Question():
    ''' хранит информацию про один вопрос'''
    def __init__(self, question=new_quest_templ, answer=new_answer_templ, 
                       wrong_answer1='', wrong_answer2='', wrong_answer3=''):
        self.question = question # вопрос
        self.answer = answer # правильный ответ
        self.wrong_answer1 = wrong_answer1 # считаем, что всегда пишется три неверных варианта
        self.wrong_answer2 = wrong_answer2 # 
        self.wrong_answer3 = wrong_answer3 #
        self.is_active = True # продолжать ли задавать этот вопрос?
        self.attempts = 0 # сколько раз этот вопрос задавался
        self.correct = 0 # количество верных ответов
    def got_right(self):
        ''' меняет статистику, получив правильный ответ'''
        self.attempts += 1
        self.correct += 1
    def got_wrong(self):
        ''' меняет статистику, получив неверный ответ'''
        self.attempts += 1

class QuestionView():
    ''' сопоставляет данные и виджеты для отображения вопроса'''
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        # конструктор получает и запоминает объект с данными и виджеты, соответствующие полям анкеты
        self.frm_model = frm_model  # может получить и None - ничего страшного не случится, 
                                    # но для метода show нужно будет предварительно обновить данные методом change
        self.question = question
        self.answer = answer
        self.wrong_answer1 = wrong_answer1
        self.wrong_answer2 = wrong_answer2
        self.wrong_answer3 = wrong_answer3  
    def change(self, frm_model):
        ''' обновление данных, уже связанных с интерфейсом '''
        self.frm_model = frm_model
    def show(self):
        ''' выводит на экран все данные из объекта '''
        self.question.setText(self.frm_model.question)
        self.answer.setText(self.frm_model.answer)
        self.wrong_answer1.setText(self.frm_model.wrong_answer1)
        self.wrong_answer2.setText(self.frm_model.wrong_answer2)
        self.wrong_answer3.setText(self.frm_model.wrong_answer3)

class QuestionEdit(QuestionView):
    ''' используется, если нужно редактировать форму: устанавливает обработчики событий, которые сохраняют текст'''
    def save_question(self):
        ''' сохраняет текст вопроса '''
        self.frm_model.question = self.question.text() # копируем данные из виджета в объект
    def save_answer(self):
        ''' сохраняет текст правильного ответа '''
        self.frm_model.answer = self.answer.text() # копируем данные из виджета в объект
    def save_wrong(self):
        ''' сохраняет все неправильные ответы 
        (если в следующей версии программы число неправильных ответов станет переменным 
        и они будут вводиться в списке, можно будет поменять этот метод) '''
        self.frm_model.wrong_answer1 = self.wrong_answer1.text()
        self.frm_model.wrong_answer2 = self.wrong_answer2.text()
        self.frm_model.wrong_answer3 = self.wrong_answer3.text()
    def set_connects(self):
        ''' устанавливает обработки событий в виджетах так, чтобы сохранять данные '''
        self.question.editingFinished.connect(self.save_question)
        self.answer.editingFinished.connect(self.save_answer)
        self.wrong_answer1.editingFinished.connect(self.save_wrong) 
        self.wrong_answer2.editingFinished.connect(self.save_wrong)
        self.wrong_answer3.editingFinished.connect(self.save_wrong)
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        # переопределим конструктор, чтобы не вызывать вручную set_connects (дети могут вызывать вручную)
        super().__init__(frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3)
        self.set_connects()

class AnswerCheck(QuestionView):
    ''' считая, что вопросы анкеты визуализируются чек-боксами, проверяет, выбран ли правильный ответ.'''
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3, showed_answer, result):
        ''' запоминает все свойства. showed_answer - это виджет, в котором записывается правильный ответ (показывается позднее)
        result - это виджет, в который будет записан txt_right либо txt_wrong'''
        super().__init__(frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3)
        self.showed_answer = showed_answer
        self.result = result
    def check(self):
        ''' ответ заносится в статистику, но переключение в форме не происходит: 
        этот класс ничего не знает про панели на форме '''
        if self.answer.isChecked():
            # ответ верный, запишем и отразим в статистике
            self.result.setText(text_correct) # надпись "верно" или "неверно"
            self.showed_answer.setText(self.frm_model.answer) # пишем сам текст ответа в соотв. виджете 
            self.frm_model.got_right() # обновить статистику, добавив один верный ответ
        else:
            # ответ неверный, запишем и отразим в статистике
            self.result.setText(text_wrong) # надпись "верно" или "неверно"
            self.showed_answer.setText(self.frm_model.answer) # пишем сам текст ответа в соотв. виджете 
            self.frm_model.got_wrong() # обновить статистику, добавив неверный ответ
            
class QuestionListModel(QAbstractListModel):
    ''' в данных находится список объектов типа Question, 
    а также список активных вопросов, чтобы показывать его на экране '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_list = []
    def rowCount(self, index):
        ''' число элементов для показа: обязательный метод для модели, с которой будет связан виджет "список"'''
        return len(self.form_list)
    def data(self, index, role):
        ''' обязательный метод для модели: какие данные она дает по запросу от интерфейса'''
        if role == Qt.DisplayRole:
            # интерфейс хочет нарисовать эту строку, дадим ему текст вопроса для отображения
            form = self.form_list[index.row()]
            return form.question
    def insertRows(self, parent=QModelIndex()):
        ''' этот метод вызывается, чтобы вставить в список объектов новые данные;
        генерируется и вставляется один пустой вопрос.'''
        position = len(self.form_list) # мы вставляем в конец, это нужно сообщить следующей строкой:
        self.beginInsertRows(parent, position, position) # вставка данных должна быть после этого указания и перед endInsertRows()
        self.form_list.append(Question()) # добавили новый вопрос в список данных
        self.endInsertRows() # закончили вставку (теперь можно продолжать работать с моделью)
        QModelIndex()
        return True # сообщаем, что все прошло хорошо
    def removeRows(self, position, parent=QModelIndex()):
        ''' стандартный метод для удаления строк - после удаления из модели строка автоматически удаляется с экрана'''
        self.beginRemoveRows(parent, position, position) # сообщаем, что мы собираемся удалять строку - от position до position 
            # (вообще говоря, стандарт метода removeRows предлагает убирать несколько строк, но мы напишем одну)
        self.form_list.pop(position) # удаляем из списка элемент с номером position
            # в правильной реализации программы удалять вопросы со статистикой нельзя, можно их деактивировать, 
            # но это заметно усложняет модель (надо поддерживать список всех вопросов для статистики 
            # и список активных для отображения в списке редактирования)
        self.endRemoveRows() # закончили удаление (дальше библиотека сама обновляет список на экране)
        return True # все в порядке 
            # (по-хорошему нам может прийти несуществующий position,
            #  правильнее было бы писать try except и возвращать True только в действительно сработавшем случае)
    def random_question(self):
        ''' Выдаёт случайный вопрос '''
        # тут стоит проверять, что вопрос активный...
        total = len(self.form_list)
        current = randint(0, total - 1)
        return self.form_list[current]

def random_AnswerCheck(list_model, w_question, widgets_list, w_showed_answer, w_result):
    '''возвращает новый экземпляр класса AnswerCheck, 
    со случайным вопросом и случайным разбросом ответов по виджетам'''
    frm = list_model.random_question()
    shuffle(widgets_list)
    frm_card = AnswerCheck(frm, w_question, widgets_list[0], widgets_list[1], widgets_list[2], widgets_list[3], w_showed_answer, w_result)
    return frm_card