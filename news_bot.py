import os
import requests

# 1. 깃허브 금고에서 토큰 가져오기
KAKAO_TOKEN = os.environ.get('KAKAO_TOKEN')

def send_kakao_message(text):
    header = {"Authorization": f"Bearer {KAKAO_TOKEN}"}
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    
    # 가장 단순한 텍스트 형태의 메시지 규격
    data = {
        "template_object": '{"object_type": "text", "text": "' + text + '", "link": {"web_url": "https://www.naver.com", "mobile_web_url": "https://www.naver.com"}}'
    }
    
    response = requests.post(url, headers=header, data=data)
    print("카카오 응답 코드:", response.status_code)
    print("카카오 응답 내용:", response.text)

if __name__ == "__main__":
    print("테스트 메시지 발송을 시작합니다.")
    send_kakao_message("안녕하세요! 깃허브 봇 테스트 메시지입니다.")
