import os
import sys
from pdf2zh import translate_pdf

def main(input_file, output_file):
    # PDF 파일 번역
    translate_pdf(input_file, output_file, source_lang='en', target_lang='ko')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python script.py <입력 파일> <출력 파일>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)