import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog as sd
import tkcalendar

# class Table(tk.Frame):
#     def __init__(self, parent=None, headings=tuple(), rows=tuple()):
#         super().__init__(parent)
#
#         table = ttk.Treeview(self, show="headings", selectmode="browse")
#         table["columns"] = headings
#         table["displaycolumns"] = headings
#
#         for head in headings:
#             table.heading(head, text=head, anchor=tk.CENTER)
#             table.column(head, anchor=tk.CENTER)
#
#         for row in rows:
#             table.insert('', tk.END, values=tuple(row))
#
#         scrolltable = tk.Scrollbar(self, command=table.yview)
#         table.configure(yscrollcommand=scrolltable.set)
#         scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
#         table.pack(expand=tk.YES, fill=tk.BOTH)

class CalendarDialog(sd.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""

    def body(self, master):
        self.calendar = tkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection_get()