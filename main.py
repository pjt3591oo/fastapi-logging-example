import logging

import uvicorn
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette_context import context
from starlette_context.middleware import ContextMiddleware

app = FastAPI()
router = APIRouter()


async def request_body(request: Request):
  print('라우터 미들웨어: request_body 시작')
  method = str(request.method)
  if method == 'POST' or method == 'PUT' or method == 'PATCH':
    # Request Body를 context에 저장
    context.update(request_body=await request.json())
  print('라우터 미들웨어: request_body 종료')

async def request_query_string(request: Request):
  print('라우터 미들웨어: request_query_string 시작')
  method = str(request.method)
  print(request.query_params.__dict__['_dict'])
  if method == 'GET':
    context.update(request_query_string= request.query_params.__dict__['_dict'])
  print('라우터 미들웨어: request_query_string 종료')


@app.middleware("http")
async def audit_log(request, call_next):
  print('앱 미들웨어 시작')
  response = await call_next(request)
  print('앱 미들웨어 종료')

  log = {
    "method": request.method,
    "url": request.url,
    "headers": request.headers,
    "request_body": {},
    "status": response.status_code,
    "response_body": b''
  }

  # Response Body 읽어오기
  async for chunk in response.body_iterator:
    log['response_body'] += chunk

  if "request_body" in context:
      log['request_body'] = context["request_body"]

  logging.info('{}'.format(log))

  # 새로운 Response 만들어 리턴
  return Response(
    content=log['response_body'],
    status_code=response.status_code,
    headers=dict(response.headers),
    media_type=response.media_type
  )


@router.post('/test')
def test(user: dict):
  print('요청 핸들러 호출')
  return {'user_id': user['user_id']}


@router.get('/test')
def test(user_id: int):
  print('요청 핸들러 호출')
  return {'user_id': user_id}


@router.post('/exception')
def test(user_id: int):
  print('요청 핸들러 호출')
  raise HTTPException(status_code=404, detail="Item not found")


app.add_middleware(ContextMiddleware)
app.include_router(router, dependencies=[Depends(request_body), Depends(request_query_string)])

if __name__ == '__main__':
  uvicorn.run(app)