from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton

class ScreenplayCard(QFrame):
    press_card = Signal()
    press_edit = Signal()
    press_delete = Signal()

    def __init__(self, pdf, parent=None):
        super().__init__(parent)
        self.pdf = pdf
        self.setObjectName("card")
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumWidth(420)
        self.setFixedHeight(110)
        self.setAttribute(Qt.WA_Hover, True)

        main = QVBoxLayout(self)    #main layout


        ## LABELS
        # TITLE LABEL
        title = pdf["title"]
        if pdf.get("year"):
            title += f" ({pdf['year']})"
        self.title_label = QLabel(title)
        self.title_label.setTextFormat(Qt.RichText)
        self.title_label.setStyleSheet("font-weight: 600; "
                                       "font-size: 14px; "
                                       "color: #000000")

        # AUTHOR LABEL
        self.author_label = QLabel(pdf.get("author", ""))
        self.author_label.setStyleSheet("font-style: italic; "
                                        "font-size: 12px; "
                                        "color: #444444;")

        # ADD LABELS TO MAIN LAYOUT
        main.addWidget(self.title_label)
        if pdf.get("author"):
            main.addWidget(self.author_label)


        ## BUTTONS
        # EDIT
        self.edit = QPushButton("Edit")
        self.edit.setFixedSize(50, 24)
        self.edit.setFixedHeight(30)
        self.edit.setCursor(Qt.PointingHandCursor)
        self.edit.clicked.connect(self.press_edit.emit)

        # DELETE
        self.delete = QPushButton("Delete")
        self.delete.setFixedSize(60, 22)
        self.delete.setFixedHeight(30)
        self.delete.setCursor(Qt.PointingHandCursor)
        self.delete.clicked.connect(self.press_delete.emit)

        # BUTTON LAYOUT
        buttons = QHBoxLayout()
        buttons.addWidget(self.edit)
        buttons.addWidget(self.delete)
        buttons.addStretch()

        main.addLayout(buttons) #add buttons to main layout


        ## STYLING OPTIONS
        # card
        self.setStyleSheet("""
            QFrame#card {
                background-color: white;
                border-radius: 8px;
            }
            QFrame#card:hover {
                background-color: #90EE90;
            }
        """)

        # edit button
        self.edit.setStyleSheet("""
            QPushButton 
                {background-color:#f1f3f5;
                border-radius: 6px;
                color: FFFFFF;}
            QPushButton:hover{background-color:#0000FF}""")

        # delete button
        self.delete.setStyleSheet("""
            QPushButton
                {background-color: #FFECEC;
                color: #A40000;
                border-radius: 6px;
                color: FFFFFF;}
            QPushButton:hover{background-color: #FF474C}""")


    # make card clickable
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.press_card.emit()
        super().mousePressEvent(event)
