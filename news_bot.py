import os
import urllib.request
import json
import xml.etree.ElementTree as ET

KAKAO_TOKEN = os.environ.get('KAKAO_TOKEN')

def get_naver_news():
    try:
        url = "https://news.google.com/rss/search?q=네이버뉴스&hl=ko&gl=KR&ceid=KR:ko"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
        root = ET.fromstring(html)
        news_list = []
        
        for item in root.findall('.//item')[:5]:
            title = item.find('title').text
            link = item.find('link').text
            news_list.append(f"• {title}\n  {link}")
            
        if not news_list:
            return "오늘의 주요 뉴스 헤드라인을 찾지 못했습니다."
            
        return "\n\n".join(news_list)
    except Exception as e:
        return f"뉴스 수집 중 오류 발생: {str(e)}"

def send_kakao_message(text):
    header = {
        "Authorization": f"Bearer {KAKAO_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    
    # 템플릿 객체 만들기
    payload = {
        "object_type": "text",
        "text": f"[오늘의 아침 뉴스]\n\n{text}",
        "link": {
            "web_url": "https://www.naver.com",
            "mobile_web_url": "https://www.naver.com"
        }
    }
    
    # urlencode 대신 f-string과 json.dumps 조합으로 한글 깨짐 원천 방지
    post_data = f"template_object={json.dumps(payload, ensure_ascii=False)}".encode('utf-8')
    
    req = urllib.request.Request(url, data=post_data, headers=header)
    
    try:
        with urllib.request.urlopen(req) as response:
            print("카카오 응답 코드:", response.status)
            print("카카오 응답 내용:", response.read().decode('utf-8'))
    except Exception as e:
        print("카카오 전송 실패:", str(e))

if __name__ == "__main__":
    print("아침 뉴스 수집을 시작합니다.")
    news_content = get_naver_news()
    send_kakao_message(news_content)
