# fastapi 로깅

```bash
$ uvicorn main:app --host 0.0.0.0 --port 8000 --workers 3 --log-config log.ini
```

## 도커

* 이미지 빌드

```bash
$ docker build . -t fastapi-my-service:0.1
```

* 컨테이너 실행

```bash
$ docker run -d -p 8000:80 --name my-service fastapi-my-service:0.1
```

## 도커 컴포즈

```bash
$ docker-compose up
```

* 백그라운드 모드

```bash
$ docker-compose up -d
```