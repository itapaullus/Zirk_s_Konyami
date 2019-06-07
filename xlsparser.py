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
        for row in vals:
            allcnt += 1
            try:
                if str(row[0]).startswith('комплекс') or str(row[0]).startswith('номер') or row[0] == '':
                    continue
                res = {
                        'reestr_id': self.id,
                        'pactnum': str(row[0]),
                        'place': str(row[1]),
                        'renter': str(row[2]),
                        'month': 'JAN',
                        'summ': row[3],
                        'phone': row[6]
                }
                ds.append(res)
                cnt += 1
            except Exception as e:
                errtext = 'Ошибка при разборе файла на строке {}'.format(str(allcnt))+': '+str(e)
                log.err_print(errtext)
                mb.showerror(errtext)
                return
        oktext = ('Файл успешно разобран. Обработано строк: {}'.format(str(cnt)))
        log.ok_print(oktext)
        return ds
        mb.showinfo('Загрузка реестра', oktext)
