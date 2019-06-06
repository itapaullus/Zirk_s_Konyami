from tkinter import *
from tkinter import simpledialog as sd
from tkinter.filedialog import askopenfilename
import tkcalendar
import sql_method as sql

# import tkSimpleDialog

def createdb():
    sql.drop_table('Reestr')
    sql.create_table('Reestr', {'reestr_id': 'integer',
                                'pactnum': 'text',
                                'place': 'text',
                                'renter': 'text',
                                'month': 'text',
                                'summ': 'real',
                                'phone': 'text'
                                }
                     )


    sql.insert('Reestr', [1,
                          'pact',
                          'placee',
                          'ivanyan',
                          'Jan',
                          1233121,
                          '+79645897062'
                          ]
               )

    if sql.isPrimary('Reestr',
                     {
                         'pactnum': 'pact'
                     }
                     ):
        sql.insert('Reestr',
                   [
                       1,
                       'pact',
                       'asd',
                       'dfsdf',
                       'Feb',
                       2123,
                       '45678'
                   ])
    else:
        print('double')

    print(
        sql.isPrimary('Reestr',
                      {
                          'pactnum': 'pact'
                       }
                      )
    )


class CalendarDialog(sd.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.calendar = tkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection_get()
        print(self.result)

def save_rate():
    rate = Tk()
    rate.title('Настройка комиссии')
    cd = CalendarDialog(rate)
    rate.geometry('480x320')
    rate.mainloop()

def load_file():
    print('SMTH')

    # name = askopenfilename(initialdir="/",
    #                        filetypes =(("XLS File", "*.xls"),("XLSX File", "*.xlsx"),("All Files","*.*")),
    #                        title = "Выберите реестр"
    #                        )
    # load = Toplevel()
    # load.grab_set()
    # load.title('Загрузка ведомости')
    # load.geometry('480x320')
    # load.mainloop()


window = Tk()
window.title('Emishyan Incorporated')
window.geometry('640x480')
main_menu = Menu(window)
# options_menu.add_command(label = 'Настройка')
# Настройка
options_menu = Menu(main_menu)
options_menu.add_command(label = 'Настройка Ведомости')
options_menu.add_command(label = 'Настройка Комиссии', command = save_rate)
options_menu.add_command(label = 'Группы')
options_menu.add_command(label = 'Пункты')
options_menu.add_command(label = 'Создать БД', command = createdb)
# Загрузка
load_menu = Menu(main_menu)
load_menu.add_command(label = 'Загрузка Ведомости', command = load_file)
# Таблица платежей
paytable_menu = Menu(main_menu)
paytable_menu.add_command(label = 'Долги на дату')
# Прием платежей
payprocess_menu = Menu(main_menu)
payprocess_menu.add_command(label = 'Ввод Платежа')
payprocess_menu.add_command(label = 'Отбор платежей')
# Отчеты
report_menu = Menu(main_menu)
report_menu.add_command(label = 'Оплаты')
main_menu.add_cascade(label = 'Настройка', menu = options_menu)
main_menu.add_cascade(label = 'Загрузка', menu = load_menu)
main_menu.add_cascade(label = 'Прием платежей', menu = payprocess_menu)
main_menu.add_cascade(label = 'Отчеты', menu = report_menu)
window.config(menu=main_menu)
window.mainloop()