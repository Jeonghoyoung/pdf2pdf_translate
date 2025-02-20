import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, QComboBox, QRadioButton, QHBoxLayout, QProgressBar, QMessageBox
import subprocess
import pdf2zh
from tqdm import tqdm

def translate_pdf(input_pdf, output_path=os.path.join(os.path.expanduser('~'), 'Downloads'), source_lang='en', target_lang='ko'):
    # 출력 파일 경로 설정
    output_file = os.path.join(output_path, os.path.basename(input_pdf).replace('.pdf', f'_{target_lang}.pdf'))
    
    # 진행 상태 표시를 위한 tqdm 설정
    with tqdm(total=100, desc="PDF 번역 중") as pbar:
        command = [
            "pdf2zh", "-li", source_lang, "-lo", target_lang, '-o', output_file, input_pdf
        ]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        if process.returncode == 0:
            pbar.update(100)  # 완료 시 progress bar를 100%로 설정
            return True, output_file
        else:
            return False, process.stderr

class PDFTranslator(QWidget):
    def __init__(self):
        super().__init__()
        self.output_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.selected_file = None  # 파일 선택 상태 추적을 위한 변수 추가
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 입력 방식 선택 라디오 버튼
        input_type_layout = QHBoxLayout()
        self.file_radio = QRadioButton('파일 선택')
        self.url_radio = QRadioButton('URL 입력')
        self.file_radio.setChecked(True)  # 기본값으로 파일 선택
        self.file_radio.toggled.connect(self.on_input_type_changed)
        self.url_radio.toggled.connect(self.on_input_type_changed)
        input_type_layout.addWidget(self.file_radio)
        input_type_layout.addWidget(self.url_radio)
        layout.addLayout(input_type_layout)

        # 파일 선택 위젯
        self.file_label = QLabel('선택된 파일: 없음')
        self.file_button = QPushButton('파일 선택')
        self.file_button.clicked.connect(self.select_file)

        # URL 입력 위젯
        self.url_label = QLabel('URL 입력:')
        self.url_input = QLineEdit()
        
        # 초기 상태 설정
        self.url_label.setEnabled(False)
        self.url_input.setEnabled(False)

        # 소스 언어 선택
        self.source_lang_label = QLabel('소스 언어:')
        self.source_lang_combo = QComboBox()
        self.source_lang_combo.addItems(['en', 'ko', 'zh'])

        # 타겟 언어 선택
        self.target_lang_label = QLabel('타겟 언어:')
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.addItems(['en', 'ko', 'zh'])

        # 저장 경로 선택 위젯
        path_layout = QHBoxLayout()
        self.path_label = QLabel(f'저장 경로: {self.output_path}')
        self.path_button = QPushButton('경로 선택')
        self.path_button.clicked.connect(self.select_output_path)
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_button)
        layout.addLayout(path_layout)

        # 진행 상태 표시바 위치 변경 및 초기 상태 설정
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        
        # 번역 버튼
        self.translate_button = QPushButton('번역 시작')
        self.translate_button.clicked.connect(self.translate)

        # 레이아웃에 위젯 추가 순서 변경
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_button)
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.source_lang_label)
        layout.addWidget(self.source_lang_combo)
        layout.addWidget(self.target_lang_label)
        layout.addWidget(self.target_lang_combo)
        layout.addWidget(self.progress_bar)  # 진행 상태바를 번역 버튼 위에 배치
        layout.addWidget(self.translate_button)

        self.setLayout(layout)
        self.setWindowTitle('PDF 번역기')
        self.setGeometry(300, 300, 500, 400)  # 윈도우 크기를 더 크게 설정

    def on_input_type_changed(self):
        # 파일 입력 위젯 활성화/비활성화
        file_enabled = self.file_radio.isChecked()
        self.file_label.setEnabled(file_enabled)
        self.file_button.setEnabled(file_enabled)
        
        # URL 입력 위젯 활성화/비활성화
        url_enabled = self.url_radio.isChecked()
        self.url_label.setEnabled(url_enabled)
        self.url_input.setEnabled(url_enabled)

    def select_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "파일 선택", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_name:
            self.file_label.setText(f'선택된 파일: {file_name}')
            self.selected_file = file_name

    def select_output_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "저장 경로 선택")
        if folder_path:
            self.output_path = folder_path
            self.path_label.setText(f'저장 경로: {self.output_path}')

    def translate(self):
        # 번역 시작 전 진행 상태바 초기화
        self.progress_bar.setValue(0)
        
        source_lang = self.source_lang_combo.currentText()
        target_lang = self.target_lang_combo.currentText()
        
        if self.file_radio.isChecked():
            input_file = getattr(self, 'selected_file', None)
            if input_file:
                try:
                    success, result = translate_pdf(
                        input_file, 
                        output_path=self.output_path,
                        source_lang=source_lang, 
                        target_lang=target_lang
                    )
                    
                    if success:
                        QMessageBox.information(self, "성공", f"번역이 완료되었습니다.\n저장 위치: {result}")
                        self.progress_bar.setValue(100)
                    else:
                        QMessageBox.critical(self, "오류", f"번역 중 오류가 발생했습니다: {result}")
                        self.progress_bar.setValue(0)
                except Exception as e:
                    QMessageBox.critical(self, "오류", f"번역 중 오류가 발생했습니다: {str(e)}")
                    self.progress_bar.setValue(0)
            else:
                QMessageBox.warning(self, "경고", "파일을 선택해주세요.")
        else:
            url = self.url_input.text()
            if url:
                QMessageBox.information(self, "알림", "URL 번역 기능은 아직 구현되지 않았습니다.")
            else:
                QMessageBox.warning(self, "경고", "URL을 입력해주세요.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = PDFTranslator()
    translator.show()
    sys.exit(app.exec_())