from tkinter import *
from tkinter.ttk import *
import xlsparser
import sql_method as sql
import zrk_info as log
from tkinter import messagebox as mb
import WindowController as wc


class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        main_menu = Menu(self)
        options_menu = Menu(main_menu)
        options_menu.add_command(label='Настройка Ведомости')
        options_menu.add_command(label='Настройка Комиссии', command=save_rate)
        options_menu.add_command(label='Группы')
        options_menu.add_command(label='Пункты')
        options_menu.add_command(label='Создать БД', command=createdb)
        # Загрузка
        load_menu = Menu(main_menu)
        load_menu.add_command(label='Загрузка Ведомости', command=load_file)
        # Таблица платежей
        paytable_menu = Menu(main_menu)
        paytable_menu.add_command(label='Долги на дату')
        # Прием платежей
        payprocess_menu = Menu(main_menu)
        payprocess_menu.add_command(label='Ввод Платежа')
        payprocess_menu.add_command(label='Отбор платежей')
        # Отчеты
        report_menu = Menu(main_menu)
        report_menu.add_command(label='Оплаты')
        main_menu.add_cascade(label='Настройка', menu=options_menu)
        main_menu.add_cascade(label='Загрузка', menu=load_menu)
        main_menu.add_cascade(label='Прием платежей', menu=payprocess_menu)
        main_menu.add_cascade(label='Отчеты', menu=report_menu)
        self.parent.title('Цирк с Конями...')
        self.parent.geometry('640x480+450+300')
        self.parent.config(menu=main_menu)
        self.parent.mainloop()


def createdb():
    conn = sql.DatabaseManager('Zirk.db')
    conn.drop_table('Reestr')
    conn.create_table('Reestr', {'reestr_id': 'text',
                                 'reestr_date': 'date',
                                 'pactnum': 'text',
                                 'place': 'text',
                                 'renter': 'text',
                                 'month': 'text',
                                 'amount': 'real',
                                 'phone': 'text'
                                 }
                      )

# class CalendarDialog(sd.Dialog):
#     """Dialog box that displays a calendar and returns the selected date"""
#
#     def body(self, master):
#         self.calendar = tkcalendar.Calendar(master)
#         self.calendar.pack()
#
#     def apply(self):
#         self.result = self.calendar.selection_get()


# def test():
#     table = wc.Table(window, headings=('aaa', 'bbb', 'ccc'), rows=((123, 456, 789), ('abc', 'def', 'ghk')))
#     table.pack(expand=YES, fill=BOTH)

def save_rate():
    rate = Tk()
    rate.title('Настройка комиссии')
    cd = wc.CalendarDialog(rate)
    rate.geometry('480x320')
    rate.mainloop()


def load_file():
    ask = wc.CalendarDialog(window)
    if ask.result is None:
        return
    elif ask.result.day != 1:
        log.err_print('Некорректная дата реестра! Допускается только первое число месяца!')
        mb.showerror('Загрузка реестра', 'Некорректная дата реестра! Допускается только первое число месяца!')
        return
    else:
        # проверим уникальность
        conn = sql.DatabaseManager('Zirk.db')
        if not conn.isPrimary('Reestr', {'Reestr_date': ask.result}):
            if not mb.askokcancel('Повторная загрузка',
                                  'Реестр за эту дату уже заагружался.\nПерезатереть ранее загруженные данные?'):
                return
            log.ok_print('Запускаем загрузку за дату: {}'.format(str(ask.result)))
    # return
    file = xlsparser.Reestr(ask.result)
    if file.path == '':
        return
    ds = file.parse()
    if ds:
        # conn = sql.DatabaseManager('Zirk.db')
        conn.delete('where reestr_date = date(\'{}\')'.format(str(ask.result)))
        for rec in ds:
            conn.insert('Reestr', rec.values())
        conn.commit()
    # table = wc.Table(window, headings=('aaa', 'bbb', 'ccc'), rows=((123, 456, 789), ('abc', 'def', 'ghk')))
    # table.pack(expand=YES, fill=BOTH)


window = Tk()
MainApplication(window).pack()
