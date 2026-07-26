import os
import requests
import json
import xml.etree.ElementTree as ET

KAKAO_TOKEN = os.environ.get('KAKAO_TOKEN')

def get_naver_news():
    try:
        url = "https://news.google.com/rss/search?q=네이버뉴스&hl=ko&gl=KR&ceid=KR:ko"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code != 200:
            return "뉴스를 불러오는 데 실패했습니다."
            
        root = ET.fromstring(response.text)
        titles = []
        
        for item in root.findall('.//item')[:3]: # 상위 3개만 깔끔하게
            title = item.find('title').text
            titles.append(f"- {title}")
            
        return "\n".join(titles)
    except Exception as e:
        return f"뉴스 수집 중 오류: {str(e)}"

def send_kakao_message(text):
    header = {
        "Authorization": f"Bearer {KAKAO_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    
    # 가장 에러 안 나는 순수 텍스트 템플릿
    payload = {
        "object_type": "text",
        "text": f"[오늘의 뉴스]\n\n{text}",
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
    news_content = get_naver_news()
    send_kakao_message(news_content)
