# 1단계: PyTorch 베이스 이미지 사용
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime AS base

# 2단계: 추가 패키지 설치
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && apt-get clean

# 작업 디렉토리 설정
WORKDIR /app

# Python 패키지 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Node.js 패키지 설치
# COPY package.json ./
# COPY package-lock.json ./
# RUN npm install

# 앱 소스 코드 추가
COPY . .

# 앱 실행 명령어 설정
CMD ["python", "main.py"]