# OCR을 위한 FastAPI 프로젝트
## 프로젝트 간단 내용
### 실행 방법
1. git clone 또는 git pull
2. root 디렉토리에 .env 생성
   1. GOOGLE_VISION_API_KEY 작성
   2. OCR_PROVIDER 작성
4. `uv sync` 명령어를 통해 의존성 설치
5. `uv run uvicorn app.main:app --reload --port 8000` 명령어를 통해 실행
6. `ctrl + c`를 통해 실행 종료

### OCR_PROVIDER에 들어갈 수 있는 구성
1. **stub**: 더미 데이터로 이루어져 있으며, 해당 내용은 파싱에 부적절한 내용으로 구성되어 있음
2. **paddle**: Paddle OCR 모델을 로드하게 되며, CPU를 많이 사용하는 모델로 EC2에는 부적절하나 Local 환경에서는 테스트 가능
3. **google**: Google Vision OCR 모델로 API 호출을 진행하며, EC2 환경에서는 `google`로 진행하는 것이 최적