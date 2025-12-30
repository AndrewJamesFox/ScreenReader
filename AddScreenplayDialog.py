from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

class AddScreenplayDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Add Screenplay")
        self.setFixedWidth(400)

        main = QVBoxLayout()  #main layout


        ## TEXT INPUT FIELDS
        # URL
        main.addWidget(QLabel("PDF URL:"))  #field text
        self.url_edit = QLineEdit()         #text input field
        main.addWidget(self.url_edit)       #add field to layout

        # Title
        main.addWidget(QLabel("Title:"))
        self.title_edit = QLineEdit()
        main.addWidget(self.title_edit)

        # Year
        main.addWidget(QLabel("Year (optional):"))
        self.year_edit = QLineEdit()
        main.addWidget(self.year_edit)

        # Author
        main.addWidget(QLabel("Author (optional):"))
        self.author_edit = QLineEdit()
        main.addWidget(self.author_edit)

        # prefill fields if editing
        if data:
            self.url_edit.setText(data.get("url", ""))
            self.title_edit.setText(data.get("title", ""))
            self.year_edit.setText(str(data.get("year", "")))
            self.author_edit.setText(data.get("author", ""))


        ## BUTTONS
        buttons = QHBoxLayout()             #button layout
        self.yes = QPushButton("OK")        #ok button
        self.no = QPushButton("Cancel")     #cancel button
        buttons.addWidget(self.yes)         #add ok button to button layout
        buttons.addWidget(self.no)          #add cancel button to button layout
        main.addLayout(buttons)             #add button layout to main layout
        self.yes.clicked.connect(self.accept)
        self.no.clicked.connect(self.reject)

        self.setLayout(main)                #assign main layout to dialog layout


    ### FUNCTIONS
    ## GET DICTIONARY DATA
    def get_data(self):
        year = self.year_edit.text().strip() #retrieve and clean year input
        #force to empty string if invalid
        if not year.isdigit():
            year = ""

        #return all dialog input values as dictionary
        return {
            "url": self.url_edit.text().strip(),
            "title": self.title_edit.text().strip(),
            "year": year,
            "author": self.author_edit.text().strip()
        }
