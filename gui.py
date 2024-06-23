from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
import algorithm


class FloatingWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel('Required format for students table: \n'
                            '| ID | Name | Mail | GPA | 1 priority | 2 priority | 3 priority | 4 priority | 5 priority |'
                            '\n\n'
                            'Required format for courses table: \n'
                            '| ID | Course | Quota |   (Quota - maximum limit of the course)\n', self)
        layout.addWidget(self.label)

        self.startButton = QPushButton('Start', self)
        self.startButton.clicked.connect(self.start_main_window)
        layout.addWidget(self.startButton)

        self.setStyleSheet("""
                    QWidget {
                        background-color: #333;
                    }
                    QPushButton {
                        background-color: #555;
                        color: white;
                        border: none;
                        padding: 10px;
                        min-width: 100px;
                    }
                    QPushButton:hover {
                        background-color: #777;
                    }
                    QPushButton:disabled {
                        background-color: #999;
                        color: #ccc;
                    }
                    QLabel {
                        color: white;
                    }
                """)

    def start_main_window(self):
        self.main_window.show()
        self.close()


class FileUploader(QWidget):
    def __init__(self):
        super().__init__()
        self.studentFile = None
        self.courseFile = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.studentButton = QPushButton('Upload Students File', self)
        self.studentButton.clicked.connect(self.upload_student_file)
        layout.addWidget(self.studentButton)

        self.courseButton = QPushButton('Upload Courses File', self)
        self.courseButton.clicked.connect(self.upload_course_file)
        layout.addWidget(self.courseButton)

        self.processButton = QPushButton('Upload files before starting the algorithm', self)
        self.processButton.clicked.connect(self.process_files)
        self.processButton.setEnabled(False)
        layout.addWidget(self.processButton)

        self.statusLabel = QLabel('No files uploaded yet', self)
        layout.addWidget(self.statusLabel)

        # Apply a stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #333;
            }
            QPushButton {
                background-color: #555;
                color: white;
                border: none;
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #777;
            }
            QPushButton:disabled {
                background-color: #999;
                color: #ccc;
            }
            QLabel {
                color: white;
            }
        """)

    def upload_student_file(self):
        self.studentFile, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Excel files (*.xlsx)")
        if self.studentFile:
            self.statusLabel.setText('Student file uploaded')
            self.check_files()

    def upload_course_file(self):
        self.courseFile, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Excel files (*.xlsx)")
        if self.courseFile:
            self.statusLabel.setText('Course file uploaded')
            self.check_files()

    def check_files(self):
        if self.studentFile and self.courseFile:
            self.processButton.setEnabled(True)
            self.processButton.setText('Start the algorithm')

    def process_files(self):
        if self.studentFile and self.courseFile:
            algorithm.process_files(self.studentFile, self.courseFile)
            self.statusLabel.setText('Files processed successfully \n'
                                     'Results.xlsx created in the same directory as the executable file')
        else:
            self.statusLabel.setText('Please upload both files before processing')

def main():
    app = QApplication([])

    uploader = FileUploader()
    floatingWindow = FloatingWindow(uploader)
    floatingWindow.show()

    app.exec_()

if __name__ == '__main__':
    main()