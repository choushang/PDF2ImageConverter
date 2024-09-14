# main.py
import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from UI import Ui_Form
import fitz

class PDFConverterApp(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pdf_path = ""  # 用于保存用户选择的 PDF 文件路径

        # 连接按钮事件
        self.pushButton.clicked.connect(self.upload_file)  # 连接上传按钮
        self.pushButton_2.clicked.connect(self.convert_pdf_to_images)  # 连接转换按钮

    def upload_file(self):
        # 弹出文件选择窗口，只能选择 PDF 文件
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        if file_dialog.exec_():
            # 获取用户选择的文件路径
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.pdf_path = selected_files[0]
                QMessageBox.information(self, "文件上传", f"已上传文件：{self.pdf_path}")

    def convert_pdf_to_images(self):
        # 检查是否已上传文件
        if not self.pdf_path:
            QMessageBox.warning(self, "警告", "请先上传一个 PDF 文件！")
            return

        # 创建输出文件夹（与 PDF 文件相同的目录）
        output_folder = os.path.join(os.path.dirname(self.pdf_path), "converted_images")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 打开 PDF 文件并进行转换
        document = fitz.open(self.pdf_path)
        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            pix = page.get_pixmap()
            image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
            pix.save(image_path)
            print(f"Saved: {image_path}")

        document.close()
        QMessageBox.information(self, "转换完成", f"PNG 图片已保存到：{output_folder}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PDFConverterApp()
    window.show()
    sys.exit(app.exec_())
