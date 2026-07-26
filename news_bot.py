import os
import requests
import json
import xml.etree.ElementTree as ET

KAKAO_TOKEN = os.environ.get('KAKAO_TOKEN')

def send_kakao_news_cards():
    try:
        url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code != 200:
            print("뉴스를 불러오는 데 실패했습니다.")
            return
            
        root = ET.fromstring(response.text)
        contents = []
        
        # 가장 핫한 기사 3개 추출해서 카드 아이템으로 만들기
        for item in root.findall('.//item')[:3]:
            title = item.find('title').text
            link = item.find('link').text
            
            # 각 기사를 카카오톡 '콘텐츠 카드' 형태로 구성
            content_item = {
                "title": title[:100],  # 제목이 너무 길면 잘릴 수 있으므로 100자 제한
                "description": "👉 터치하여 기사 원문 보기",
                "link": {
                    "web_url": link,
                    "mobile_web_url": link
                }
            }
            contents.append(content_item)
            
        if not contents:
            print("수집된 뉴스가 없습니다.")
            return

        header = {
            "Authorization": f"Bearer {KAKAO_TOKEN}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        api_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        
        # 카카오톡 '리스트 템플릿(list)'을 사용하여 깔끔한 카드 형태로 전송
        payload = {
            "object_type": "list",
            "header_title": "[실시간 핫이슈 TOP 3]",
            "header_link": {
                "web_url": "https://www.google.com",
                "mobile_web_url": "https://www.google.com"
            },
            "contents": contents
        }
        
        data = {
            "template_object": json.dumps(payload, ensure_ascii=False)
        }
        
        res = requests.post(api_url, headers=header, data=data)
        print("카카오 응답 코드:", res.status_code)
        print("카카오 응답 내용:", res.text)
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    print("카드형 뉴스 전송을 시작합니다.")
    send_kakao_news_cards()
