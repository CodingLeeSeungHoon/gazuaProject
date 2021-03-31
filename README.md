# gazuaProject

⚡ crawl announcement data from upbit, trade cryptocurrency through upbit OpenAPI

upbit의 프로젝트 공시 정보를 자동으로 수집해 upbit의 OpenAPI를 통해 자동으로 투자하는
알고리즘 트레이딩 프로젝트

진행상황
- 2021.03.11 비동기식 Ajax 통신 URL 캐치 성공, 공시 정보 JSON Data 추출 성공(@이승훈)
- 03.12 avoid bot detection : random sleep, random user-agent testing(@이승훈, 김준태)
- 03.24~ 구매, 판매 기능, 예외 및 통신 오류에 대한 대처 구현(@이승훈, 김준태)
- 04.01 testmain에서 임의 공시로 테스트, 오류 수정 및 테스트 진행 : 
큰 오류 없이 투자 사이클을 도는 것을 확인! 추가 테스트 필요.

진행예정
- 04.01~ Docker, AWS를 활용해 자동투자 시스템 구축
- 공시알고리즘 외 데이터 분석 + 강화학습을 활용한 투자 모델 고려
- 여러 알고리즘을 동시에 굴리는 방법 고안.