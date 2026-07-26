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
        
        for item in root.findall('.//item')[:3]:
            title = item.find('title').text
            rss_link = item.find('link').text
            
            # 진짜 언론사 원본 주소로 완벽히 변환
            real_link = rss_link
            try:
                res_redirect = requests.get(rss_link, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True, timeout=3)
                if res_redirect.url:
                    real_link = res_redirect.url
            except:
                pass
            
            # 텍스트에는 링크를 아예 적지 않고, 카드 자체의 링크 기능(web_url)에 진짜 주소를 숨김
            content_item = {
                "title": title[:100],
                "description": "👉 터치하여 기사 원문 보기",
                "link": {
                    "web_url": real_link,
                    "mobile_web_url": real_link
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
    print("깔끔한 카드형 원문 연동 전송을 시작합니다.")
    send_kakao_news_cards()
