import os
import requests
from bs4вання import BeautifulSoup

# 1. 깃허브 금고에서 카카오 토큰 가져오기
KAKAO_TOKEN = os.environ.get('KAKAO_TOKEN')

def get_naver_news():
    # 네이버 주요 뉴스 페이지 크롤링
    url = "https://news.naver.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return "뉴스를 불러오는 데 실패했습니다."
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 주요 뉴스 제목과 링크 수집
    news_list = []
    # 네이버 뉴스 메인 헤드라인 구조에 맞춘 선택자
    titles = soup.select('.cjs_headline_a')[:5] # 상위 5개만
    
    for title in titles:
        text = title.get_text().strip()
        link = title.attrs.get('href')
        news_list.append(f"• {text}\n  {link}")
        
    if not news_list:
        return "오늘의 주요 뉴스 헤드라인을 찾지 못했습니다."
        
    return "\n\n".join(news_list)

def send_kakao_message(text):
    header = {"Authorization": f"Bearer {KAKAO_TOKEN}"}
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    
    # 카카오톡 메시지 규격 (본문에 뉴스 담기)
    data = {
        "template_object": f'{{"object_type": "text", "text": "[오늘의 아침 뉴스]\\n\\n{text}", "link": {{"web_url": "https://news.naver.com", "mobile_web_url": "https://news.naver.com"}}}}'
    }
    
    response = requests.post(url, headers=header, data=data)
    print("카카오 응답 코드:", response.status_code)
    print("카카오 응답 내용:", response.text)

if __name__ == "__main__":
    print("아침 뉴스 크롤링을 시작합니다.")
    news_content = get_naver_news()
    send_kakao_message(news_content)
