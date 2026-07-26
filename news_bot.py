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
        
        # 가장 핫한 기사 5개로 변경 ([:5])
        for item in root.findall('.//item')[:5]:
            title = item.find('title').text
            rss_link = item.find('link').text
            
            # 구글 우회 링크에서 진짜 원본 기사 URL 추출 시도
            real_link = rss_link
            try:
                res_redirect = requests.get(rss_link, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True, timeout=3)
                real_link = res_redirect.url
            except:
                pass
            
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
            "header_title": "[실시간 핫이슈 TOP 5]",
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
    print("원격 링크 변환 5개 카드형 뉴스 전송을 시작합니다.")
    send_kakao_news_cards()
