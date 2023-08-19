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

### LB - 가중치 설정

```
user  nginx;
worker_processes  auto;
error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
  include       /etc/nginx/mime.types;
  default_type  application/octet-stream;

	# API 서버 업스트림
  upstream api-server {
    server api-1:80 weight=3;
    server api-2:80 weight=1;
  }

  server {
    listen 8080;

    # /api 경로로 요청된 트래픽은 업스트림 api-server로 전달
    location / {
        proxy_pass http://api-server;
    }

  }

  log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
  access_log  /var/log/nginx/access.log  main;

  sendfile        on;
  keepalive_timeout  65;
  include /etc/nginx/conf.d/*.conf;
}
```
