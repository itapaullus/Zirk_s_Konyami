from tkinter.filedialog import askopenfilename
import xlrd, xlwt
import zrk_info as log
import uuid

from tkinter import messagebox as mb

class Reestr:
    def __init__(self):
        print('init')
        self.path = askopenfilename(initialdir=r"D:\PycharmProjects\Zirk_s_Konyami",
                                    filetypes =(("XLS File", "*.xls, *.xlsx"),("XLSX File", "*.xlsx"),("All Files","*.*")),
                                    title = "Выберите реестр"
                               )
        self.id = uuid.uuid4()

    def parse(self):
        file = xlrd.open_workbook(self.path)
        sheet = file.sheet_by_index(0)
        vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
        ds = []
        cnt = 0
        allcnt = 0
        # Ищем позицию строки Итого
        #
        for row in vals:
            if str(row[0]) == 'номер':
                try:
                    posTotal = row.index('итого:')
                    break
                except ValueError as e:
                    errtext = 'Некорректный формат файла. Не найден столбец "итого:"'
                    log.err_print(errtext)
                    mb.showerror('Загрузка реестра', errtext)
                    return
        else:
            errtext = 'Некорректный формат файла. Не найдена шапка таблицы!"'
            log.err_print(errtext)
            mb.showerror('Загрузка реестра', errtext)
            return

        for row in vals:
            allcnt += 1
            try:
                if str(row[0]).startswith('комплекс') or str(row[0]).startswith('номер') or row[0] == '':
                    continue
                total = 0.0
                for sums in range(3, posTotal):
                    total += float(row[sums] or 0)
                    res = {
                            'reestr_id': self.id,
                            'pactnum': str(row[0]),
                            'place': str(row[1]),
                            'renter': str(row[2]),
                            'month': 'JAN',
                            'summ': row[sums],
                            'phone': row[6]
                    }
                    ds.append(res)
                    cnt += 1
                if total != row[5]:
                    errtext = 'Ошибка в строке {}: поле "Итого" {} не соответствует сумме платежей {}'.format(row[2], row[5], str(total))
                    log.err_print(errtext)
                    mb.showerror('Загрузка реестра', errtext)
                    return
            except Exception as e:
                errtext = 'Ошибка при разборе файла на строке {}'.format(str(allcnt))+': '+str(e)
                log.err_print(errtext)
                mb.showerror('Загрузка реестра', errtext)
                return
        oktext = ('Файл успешно разобран. Обработано строк: {}'.format(str(cnt)))
        log.ok_print(oktext)
        mb.showinfo('Загрузка реестра', oktext)
        return ds

