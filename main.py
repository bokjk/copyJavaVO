import os
import shutil
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QPlainTextEdit
from PySide6.QtCore import QThread, Signal

class CopyThread(QThread):
    message = Signal(str)

    def __init__(self, src, dst):
        super().__init__()
        self.src = src
        self.dst = dst

    def run(self):
        self.copy_folders(self.src, self.dst, ['vo', 'entity'])

    def copy_folders(self, src, dst, folder_names):
        for dirpath, dirnames, filenames in os.walk(src):
            for folder_name in folder_names:
                if folder_name in dirnames:
                    folder_src = os.path.join(dirpath, folder_name)
                    folder_dst = os.path.join(dst, os.path.relpath(dirpath, src), folder_name)
                    os.makedirs(folder_dst, exist_ok=True)
                    for filename in os.listdir(folder_src):
                        filepath_src = os.path.join(folder_src, filename)
                        filepath_dst = os.path.join(folder_dst, filename)
                        shutil.copy(filepath_src, filepath_dst)
                        self.message.emit(f'Copied file: {filepath_src} to {filepath_dst}')
        self.message.emit('Copying completed')

class FolderCopyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.label_src = QLabel('Source Folder: Not selected')
        self.label_dst = QLabel('Target Folder: Not selected')
        self.button_src = QPushButton('Select Source Folder')
        self.button_dst = QPushButton('Select Target Folder')
        self.button_copy = QPushButton('Start Copy')
        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.layout.addWidget(self.label_src)
        self.layout.addWidget(self.button_src)
        self.layout.addWidget(self.label_dst)
        self.layout.addWidget(self.button_dst)
        self.layout.addWidget(self.button_copy)
        self.layout.addWidget(self.log_view)
        self.setLayout(self.layout)
        
        self.button_src.clicked.connect(self.select_source_folder)
        self.button_dst.clicked.connect(self.select_target_folder)
        self.button_copy.clicked.connect(self.start_copy)
        
    def select_source_folder(self):
        folder = QFileDialog.getExistingDirectory()
        if folder:
            self.src_folder = folder
            self.label_src.setText(f'Source Folder: {folder}')

    def select_target_folder(self):
        folder = QFileDialog.getExistingDirectory()
        if folder:
            self.dst_folder = folder
            self.label_dst.setText(f'Target Folder: {folder}')

    def start_copy(self):
        if hasattr(self, 'src_folder') and hasattr(self, 'dst_folder'):
            self.copy_thread = CopyThread(self.src_folder, self.dst_folder)
            self.copy_thread.message.connect(self.log_view.appendPlainText)
            self.copy_thread.start()

app = QApplication([])
window = FolderCopyWidget()
window.show()
app.exec_()
