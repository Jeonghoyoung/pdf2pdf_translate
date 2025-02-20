import os
import sys
import subprocess
from tqdm import tqdm

def translate_pdf(input_pdf, output_path=os.path.join(os.path.expanduser('~'), 'Downloads'), source_lang='en', target_lang='ko'):
    # 출력 파일 경로 설정
    output_file = os.path.join(output_path, os.path.basename(input_pdf).replace('.pdf', f'_{target_lang}.pdf'))
    
    # 진행 상태 표시를 위한 tqdm 설정
    with tqdm(total=100, desc="PDF 번역 중") as pbar:
        command = [
            "pdf2zh", "-li", source_lang, "-lo", target_lang, input_pdf
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # 진행률 업데이트 (예시: 10% 단위로)
                pbar.update(10)
        
        returncode = process.poll()
        
        if returncode == 0:
            pbar.update(100)  # 완료 시 progress bar를 100%로 설정
            return True, output_file
        else:
            error_msg = process.stderr.read()
            return False, error_msg

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python script.py <입력 파일> <출력 파일>")
        sys.exit(1)
    input_file = sys.argv[1]
    # output_path = sys.argv[2]
    translate_pdf(input_file)