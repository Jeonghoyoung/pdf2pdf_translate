import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, QComboBox
from pdf2zh import translate_pdf

class PDFTranslator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 파일 선택 버튼
        self.file_label = QLabel('선택된 파일: 없음')
        self.file_button = QPushButton('파일 선택')
        self.file_button.clicked.connect(self.select_file)

        # URL 입력
        self.url_label = QLabel('URL 입력:')
        self.url_input = QLineEdit()

        # 소스 언어 선택
        self.source_lang_label = QLabel('소스 언어:')
        self.source_lang_combo = QComboBox()
        self.source_lang_combo.addItems(['en', 'ko', 'zh'])

        # 타겟 언어 선택
        self.target_lang_label = QLabel('타겟 언어:')
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.addItems(['en', 'ko', 'zh'])

        # 번역 버튼
        self.translate_button = QPushButton('번역 시작')
        self.translate_button.clicked.connect(self.translate)

        # 레이아웃에 위젯 추가
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_button)
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.source_lang_label)
        layout.addWidget(self.source_lang_combo)
        layout.addWidget(self.target_lang_label)
        layout.addWidget(self.target_lang_combo)
        layout.addWidget(self.translate_button)

        self.setLayout(layout)
        self.setWindowTitle('PDF 번역기')
        self.setGeometry(300, 300, 400, 200)

    def select_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "파일 선택", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_name:
            self.file_label.setText(f'선택된 파일: {file_name}')
            self.selected_file = file_name

    def translate(self):
        source_lang = self.source_lang_combo.currentText()
        target_lang = self.target_lang_combo.currentText()
        input_file = getattr(self, 'selected_file', None)
        url = self.url_input.text()

        if input_file:
            output_file = input_file.replace('.pdf', f'_{target_lang}.pdf')
            translate_pdf(input_file, output_file, source_lang=source_lang, target_lang=target_lang)
            print(f'번역 완료: {output_file}')
        elif url:
            # URL을 통한 번역 로직 추가 필요
            print(f'URL 번역 기능은 아직 구현되지 않았습니다: {url}')
        else:
            print('파일이나 URL을 입력하세요.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = PDFTranslator()
    translator.show()
    sys.exit(app.exec_())