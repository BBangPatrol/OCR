FROM python:3.12-slim

WORKDIR /app

# uv 설치
RUN pip install --no-cache-dir uv

# 의존성 파일 먼저 복사
COPY pyproject.toml uv.lock ./

# 의존성 설치
RUN uv sync --frozen --no-dev

# 애플리케이션 코드 복사
COPY app ./app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]