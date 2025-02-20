import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

# 파파고 API 키 가져오기
client_id = os.getenv('PAPAGO_CLIENT_ID')
client_secret = os.getenv('PAPAGO_CLIENT_SECRET')

def translate_text(text, source, target):
    url = "https://openapi.naver.com/v1/papago/n2mt"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    data = {
        "source": source,
        "target": target,
        "text": text
    }
    
    response = requests.post(url, headers=headers, data=data)
    result = json.loads(response.text)
    
    return result['message']['result']['translatedText']

def main():
    st.title("파파고 번역기")
    
    # 언어 선택 옵션
    languages = {
        '한국어': 'ko',
        '영어': 'en',
        '일본어': 'ja',
        '중국어 간체': 'zh-CN',
        '중국어 번체': 'zh-TW',
        '베트남어': 'vi',
        '인도네시아어': 'id',
        '태국어': 'th',
        '독일어': 'de',
        '러시아어': 'ru',
        '스페인어': 'es',
        '이탈리아어': 'it',
        '프랑스어': 'fr'
    }
    
    # 두 개의 컬럼 생성
    col1, col2 = st.columns(2)
    
    with col1:
        source_lang = st.selectbox(
            "원본 언어 선택",
            options=list(languages.keys()),
            index=0
        )
    
    with col2:
        target_lang = st.selectbox(
            "목표 언어 선택",
            options=list(languages.keys()),
            index=1
        )
    
    # 텍스트 입력 영역
    text_input = st.text_area("번역할 텍스트를 입력하세요:", height=150)
    
    if st.button("번역하기"):
        if text_input:
            try:
                # 선택된 언어의 코드 가져오기
                source_code = languages[source_lang]
                target_code = languages[target_lang]
                
                # 번역 수행
                translated = translate_text(text_input, source_code, target_code)
                
                # 결과 표시
                st.success("번역 완료!")
                st.write("번역 결과:")
                st.write(translated)
                
            except Exception as e:
                st.error(f"번역 중 오류가 발생했습니다: {str(e)}")
        else:
            st.warning("번역할 텍스트를 입력해주세요.")

if __name__ == "__main__":
    main()