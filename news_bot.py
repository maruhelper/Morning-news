import os
import requests
import json
import xml.etree.ElementTree as ET

KAKAO_TOKEN = os.environ.get('KAKAO_TOKEN')

def send_kakao_news_text():
    try:
        url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code != 200:
            print("뉴스를 불러오는 데 실패했습니다.")
            return
            
        root = ET.fromstring(response.text)
        news_lines = []
        
        for i, item in enumerate(root.findall('.//item')[:3], 1):
            title = item.find('title').text
            rss_link = item.find('link').text
            
            # 진짜 원본 주소 추출
            real_link = rss_link
            try:
                res_redirect = requests.get(rss_link, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True, timeout=3)
                if res_redirect.url:
                    real_link = res_redirect.url
            except:
                pass
            
            # 긴 URL 주소를 숨기고 깔끔한 제목과 '[원문보기]' 텍스트로 구성
            news_lines.append(f"{i}. {title}\n🔗 {real_link}")
            
        if not news_lines:
            print("수집된 뉴스가 없습니다.")
            return

        header = {
            "Authorization": f"Bearer {KAKAO_TOKEN}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        api_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        
        # 카카오톡 기본 텍스트 메시지 형식 (모바일에서 링크 터치 시 100% 작동)
        payload = {
            "object_type": "text",
            "text": "[실시간 핫이슈 TOP 3]\n\n" + "\n\n".join(news_lines),
            "link": {
                "web_url": "https://www.google.com",
                "mobile_web_url": "https://www.google.com"
            }
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
    print("최종 링크 보장형 뉴스 전송을 시작합니다.")
    send_kakao_news_text()
