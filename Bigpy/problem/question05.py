"""
문제 5 (난이도 상) — 종합: API + 동적크롤링 + 엑셀(이미지 포함) 저장 + 자동화
1) TMDB API로 인기 영화 TOP 5 (제목/평점/개봉일/포스터) 조회
2) Playwright로 각 영화 제목을 네이버에 검색해서 노출되는 평점/리뷰 정보 크롤링
3) 두 결과를 영화 제목 기준으로 합쳐서 엑셀(xlsx)로 저장 (포스터 이미지 삽입)
4) 파일 맨 아래에 배치파일 + 작업 스케줄러 등록 방법 주석으로 안내

사전 준비:
1. TMDB에서 API 키 발급 → .env에 TMDB_API_KEY=... 저장
2. 설치: uv pip install python-dotenv requests playwright xlsxwriter beautifulsoup4
3. playwright install chromium (최초 1회)
"""


