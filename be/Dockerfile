# 베이스 이미지로 Python 3.10 사용
FROM python:3.10-slim AS builder

# 작업 디렉토리 설정
WORKDIR /django

# 의존성 파일을 복사하고 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

# 애플리케이션 파일을 복사
COPY . .

FROM python:3.10-slim
WORKDIR /django
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .
