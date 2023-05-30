import os
import shutil
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

def copy_vo_folder(src, dst):
    for dirpath, dirnames, filenames in os.walk(src):
        if 'vo' in dirnames:
            vo_src = os.path.join(dirpath, 'vo')
            vo_dst = os.path.join(dst, os.path.relpath(dirpath, src), 'vo')
            os.makedirs(vo_dst, exist_ok=True)
            for filename in os.listdir(vo_src):
                filepath_src = os.path.join(vo_src, filename)
                filepath_dst = os.path.join(vo_dst, filename)
                shutil.copy(filepath_src, filepath_dst)

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
        self.layout.addWidget(self.label_src)
        self.layout.addWidget(self.button_src)
        self.layout.addWidget(self.label_dst)
        self.layout.addWidget(self.button_dst)
        self.layout.addWidget(self.button_copy)
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
            copy_vo_folder(self.src_folder, self.dst_folder)

app = QApplication([])
window = FolderCopyWidget()
window.show()
app.exec_()
