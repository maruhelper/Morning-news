import os
import requests
import json
import xml.etree.ElementTree as ET

KAKAO_TOKEN = os.environ.get('KAKAO_TOKEN')

def get_hot_news():
    try:
        # 특정 키워드 없이 구글 뉴스 한국 실시간 전체 헤드라인 수집
        url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code != 200:
            return "뉴스를 불러오는 데 실패했습니다."
            
        root = ET.fromstring(response.text)
        news_list = []
        
        # 가장 핫한 최신 기사 딱 3개만 추출
        for item in root.findall('.//item')[:3]:
            title = item.find('title').text
            link = item.find('link').text
            news_list.append(f"• {title}\n  🔗 {link}")
            
        if not news_list:
            return "실시간 주요 뉴스 헤드라인을 찾지 못했습니다."
            
        return "\n\n".join(news_list)
    except Exception as e:
        return f"뉴스 수집 중 오류: {str(e)}"

def send_kakao_message(text):
    header = {
        "Authorization": f"Bearer {KAKAO_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    
    payload = {
        "object_type": "text",
        "text": f"[실시간 핫이슈 TOP 3]\n\n{text}",
        "link": {
            "web_url": "https://www.naver.com",
            "mobile_web_url": "https://www.naver.com"
        }
    }
    
    data = {
        "template_object": json.dumps(payload, ensure_ascii=False)
    }
    
    res = requests.post(url, headers=header, data=data)
    print("카카오 응답 코드:", res.status_code)
    print("카카오 응답 내용:", res.text)

if __name__ == "__main__":
    print("실시간 핫이슈 수집 및 전송을 시작합니다.")
    news_content = get_hot_news()
    send_kakao_message(news_content)
