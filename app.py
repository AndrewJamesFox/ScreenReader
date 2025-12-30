import sys
import os
import re
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QVBoxLayout, QWidget, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt
from storage import load_library, save_library
from library import download_pdf
from reader import PDFReader
from AddScreenplayDialog import AddScreenplayDialog
from ScreenplayCard import ScreenplayCard


class ScreenReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.library = load_library()           #load library data

        ## SCREENPLAY LIST
        self.scroll = QScrollArea()             #create scrollable area
        self.scroll.setWidgetResizable(True)    #allows auto resizing
        self.box = QWidget()                    #container (box) widget for PDF cards
        self.cards = QVBoxLayout()              #create vertical layout for cards
        self.cards.setSpacing(8)                #space between cards
        self.cards.setAlignment(Qt.AlignTop)    #align cards at top
        self.box.setLayout(self.cards)          #assign layout to container
        self.scroll.setWidget(self.box)         #set container as scroll area content

        for sp in self.library["screenplays"]:  #populate scroll area with screenplays
            self.add_card(sp)


        ## ADD PDF BUTTON
        add_btn = QPushButton("Add Screenplay") #add Add button
        add_btn.clicked.connect(self.add_pdf)   #connect click to add_screenplay()


        ## MAIN LAYOUT
        main = QVBoxLayout()                    #create main layout
        main.addWidget(self.scroll)             #add scrollable area to main
        main.addWidget(add_btn)                 #add Add button
        mbox = QWidget()                        #central (box) widget to hold main layout
        mbox.setLayout(main)                    #assign main to mbox
        self.setCentralWidget(mbox)             #set central widget of main window

        self.setWindowTitle("ScreenReader")     #set title of window
        self.resize(500, 700)                   #set window size


    ### FUNCTIONS
    ## ADD CARD TO LAYOUT
    def add_card(self, pdf):
        """Adds card button to layout."""
        card = ScreenplayCard(pdf)
        card.press_card.connect(lambda pdf=pdf: self.open_pdf(pdf, card))
        card.press_edit.connect(lambda pdf=pdf, c=card: self.edit_pdf(pdf, c))
        card.press_delete.connect(lambda pdf=pdf, c=card: self.delete_pdf(pdf, c))
        self.cards.addWidget(card)


    ## ADD PDF
    def add_pdf(self):
        dialog = AddScreenplayDialog(self)
        if dialog.exec() != AddScreenplayDialog.Accepted:
            return

        #retrieve entered data, requiring URL and title
        data = dialog.get_data()
        url = data["url"]
        title = data["title"]
        year = data["year"]
        author = data["author"]
        if not url or not title:
            return

        #create identifier for file from title
        temp_title = title.lower()
        temp_title = re.sub(r'[^\w\s-]', '', temp_title)  #remove non-word chars, keeping spaces and hyphens
        safe_title = re.sub(r'[-\s]+', '_', temp_title).strip('_')  #replace spaces/hyphens with single underscore
        filename = f"{safe_title}.pdf"

        #try to download file
        try:
            file_path = download_pdf(url, filename)
        except Exception as e:
            #show error if download fails
            QMessageBox.critical(self, "Download Failed", str(e))
            return

        #create entry for library
        entry = {"id": safe_title,
                 "title": title,
                 "year": year,
                 "author": author,
                 "url": url,
                 "file_path": file_path,
                 "last_page": 0
                 }
        self.library["screenplays"].append(entry)   #add entry to library
        save_library(self.library)                  #save library
        self.add_card(entry)                        #add new card to layout


    ## DELETE PDF
    def delete_pdf(self, pdf, card):
        reply = QMessageBox.question(
            self,
            "Delete Screenplay",
            f"Are you sure you want to delete:\n\n{pdf['title']}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # Remove PDF file
        file_path = pdf.get("file_path")
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "File Error",
                    f"Could not delete PDF:\n{e}"
                )

        #remove from library
        self.library["screenplays"].remove(pdf)
        save_library(self.library)

        #remove card from UI
        card.setParent(None)
        card.deleteLater()


    ## OPEN PDF
    def open_pdf(self, pdf, card):
        #calls when page changes
        def on_page_change(page):
            pdf["last_page"] = page     #update last-read page
            save_library(self.library)  #save updated library immediately

        #create and show new PDF reader window
        self.reader = PDFReader(
            pdf_path=pdf["file_path"],
            start_page=pdf.get("last_page", 0),
            on_page_change=on_page_change
        )
        self.reader.show()


    ## EDIT PDF
    def edit_pdf(self, pdf, card):
        dialog = AddScreenplayDialog(self, data=pdf)

        if dialog.exec() != AddScreenplayDialog.Accepted:
            return

        updated = dialog.get_data()

        #update screenplay fields
        pdf["title"] = updated["title"]
        pdf["year"] = updated["year"]
        pdf["author"] = updated["author"]
        pdf["url"] = updated["url"]

        save_library(self.library)

        #update UI labels
        title = pdf["title"]
        if pdf.get("year"):
            title += f" ({pdf['year']})"

        card.title_label.setText(title)
        card.author_label.setText(pdf.get("author", ""))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenReaderApp()
    window.show()
    sys.exit(app.exec())