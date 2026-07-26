import os
import requests
import json
import xml.etree.ElementTree as ET

KAKAO_TOKEN = os.environ.get('KAKAO_TOKEN')

def send_kakao_news_cards():
    try:
        # 네이버 뉴스 RSS를 사용하여 확실한 원본 언론사 링크 확보
        url = "https://news.google.com/rss/search?q=뉴스&hl=ko&gl=KR&ceid=KR:ko"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code != 200:
            print("뉴스를 불러오는 데 실패했습니다.")
            return
            
        root = ET.fromstring(response.text)
        contents = []
        
        for item in root.findall('.//item')[:3]:
            title = item.find('title').text
            rss_link = item.find('link').text
            
            # 우회 링크를 풀어서 진짜 원본 주소 찾기
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
            "header_title": "[실시간 핫이슈 TOP 3]",
            "header_link": {
                "web_url": "https://www.naver.com",
                "mobile_web_url": "https://www.naver.com"
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
    print("링크 원문 연결 3개 카드형 뉴스 전송을 시작합니다.")
    send_kakao_news_cards()
