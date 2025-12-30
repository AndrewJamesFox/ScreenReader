from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QKeySequence, QShortcut

#inherits from QMainWindow
class PDFReader(QMainWindow):
    def __init__(self, pdf_path, start_page, on_page_change):
        super().__init__()
        self.on_page_change = on_page_change    #store callback func for page changes

        ## PDF VIEW
        self.document = QPdfDocument(self)  #create object to hold PDF
        self.document.load(pdf_path)        #load PDF from disk
        self.view = QPdfView(self)                                #widget to display PDF
        (self.view.setDocument(self.document))                    #attach PDF to view
        (self.view.setZoomMode(QPdfView.ZoomMode.FitInView))      #scale PDF so it fits
        (self.view.pageNavigator().jump(start_page, QPointF(0,0)))#jump to starting page
        (self.view.pageNavigator().currentPageChanged.
         connect(self.page_changed))                              #connect page-change to handler method


        ## NAVIGATION BUTTONS
        bwd = QPushButton("Previous (Left, Tab)")   #create buttons
        fwd = QPushButton("Next (Right, Enter, Space)")
        bwd.clicked.connect(self.pg_bwd)            #connect buttons to clicks
        fwd.clicked.connect(self.pg_fwd)
        buttons = QHBoxLayout()                     #buttons layout
        buttons.addWidget(bwd)                      #add buttons to buttons layout
        buttons.addWidget(fwd)


        ## MAIN LAYOUT
        main = QVBoxLayout()        #main layout
        main.addWidget(self.view)   #add PDF view to layout
        main.addLayout(buttons)     #add button layout

        box = QWidget()             #container (box) widget to hold main layout
        box.setLayout(main)         #assign main layout to box
        self.setCentralWidget(box)  #set box to central widget of main window
        self.showMaximized()        #show reader maximized


        ## KEYBOARD SHORTCUTS
        QShortcut(QKeySequence(Qt.Key_Right), self, activated=self.pg_fwd)  #arrow right
        QShortcut(QKeySequence(Qt.Key_Return), self, activated=self.pg_fwd) #enter
        QShortcut(QKeySequence(Qt.Key_Space), self, activated=self.pg_fwd)  #space
        QShortcut(QKeySequence(Qt.Key_Left), self, activated=self.pg_bwd)   #arrow left
        QShortcut(QKeySequence(Qt.Key_Tab), self, activated=self.pg_bwd)    #shift
        QShortcut(QKeySequence(Qt.Key_Escape), self, activated=self.close)  #escape to close
        QShortcut(QKeySequence(Qt.Key_F), self, activated=self.window_toggle)#f for window mode toggle


    ### FUNCTIONS
    ## PAGE CHANGE
    def page_changed(self, page):
        self.on_page_change(page)   #callback func with new page number to save page progress.


    ## PAGE FORWARD
    def pg_fwd(self):
        current = self.view.pageNavigator().currentPage()               #get current page number
        if current < self.document.pageCount() - 1:                     #not already on last page?
            self.view.pageNavigator().jump(current + 1, QPointF(0, 0))  #then jump to next page


    ## PAGE BACKWARD
    def pg_bwd(self):
        current = self.view.pageNavigator().currentPage()               #get current page number
        if current > 0:                                                 #not already on first page?
            self.view.pageNavigator().jump(current - 1, QPointF(0, 0))  #then jump to previous page

    ## TOGGLE WINDOW MODE
    def window_toggle(self):
        if self.isMaximized():
            self.showFullScreen()
        else:
            self.showMaximized()

    ## ON CLOSE
    def closeEvent(self, event):
        super().closeEvent(event)

