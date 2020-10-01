"""
Merges PDF's
"""
import toga
import re
from PyPDF2 import PdfFileMerger
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pathlib import Path


def sorted_nicely(l): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

class pdfmerge(toga.App):
    def startup(self):
        self.db = {}
        self.root = None
        main_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                width=250,
                height=600
            )
        )

        self.pdf_tree = toga.Table(
            headings = ['File'],
            data = [],
            on_double_click=self.rm_row,
            style=Pack(padding=5, width=250, height=600)
        )

        self.select_btn = toga.Button(
            'browse', on_press=self.select_cb,
            style=Pack(padding=5, width=120)
        )

        self.merge_btn = toga.Button(
            'merge', on_press=self.merge_cb,
            style=Pack(padding=5, width=120)
        )

        info_panel = toga.Box(style=Pack(direction=ROW))
        info_panel.add(self.pdf_tree)

        button_panel = toga.Box(style=Pack(direction=ROW))
        button_panel.add(self.select_btn)
        button_panel.add(self.merge_btn)

        main_box.add(info_panel)
        main_box.add(button_panel)
        self.main_window = toga.MainWindow(
            title=self.formal_name,
            size=(250, 600)
        )
        self.main_window.content = main_box
        self.main_window.show()

    def select_cb(self, btn):
        p = self.main_window.select_folder_dialog('Locate PDFs')
        if len(p) != 0:
            pdfs = Path(p[0]).rglob("*.pdf")
            self.root = Path(p[0]).resolve()
            for x in pdfs:
                self.db[str(x.name)] = x

            self.data = [k for k in self.db]
            self.data = sorted_nicely(self.data)
            print(self.data)
            for i, x in enumerate(self.data):
                self.pdf_tree.data.insert(i, x)

    def merge_cb(self, btn):
        merge = PdfFileMerger()
        if self.data:
            for x in self.data:
                merge.append(str(self.db[x]))

        out = str(self.root / "merged.pdf")
        merge.write(out)

    def rm_row(self, table, row):
        table.data.remove(row)
        rm = self.db.pop(row.file, None)
        self.data.remove(row.file)


def main():
    return pdfmerge()
