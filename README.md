# 2024-DRF-board-project

## 📒 목차
- [API 명세서](#📍-API-명세서)
- [설치 및 실행 방법](#📍-설치-및-실행-방법)
- [디렉토리 구조](#📍-디렉토리-구조)
- [과제에 적용하고 싶었던 부분](#📍-과제에-적용하고-싶었던-부분)
- [과제에 대한 회고](#📍-과제에-대한-회고)


## 📍 API 명세서
- [포스트맨 API 명세서](https://documenter.getpostman.com/view/18212819/2sA3XWbHvJ)


## 📍 설치 및 실행 방법
1. 해당 프로젝트를 clone하고, 프로젝트로 들어간다.
    - [깃허브 바로가기](https://github.com/Odreystella/2024-DRF-board-project)


2. 루트 디렉토리에 `.env` 파일 추가한다.
    ```shell
    # django 환경변수
    DJANGO_SECRET_KEY=django-insecure-4765aa!*gwk3jah-13af39kpcv%w2in4suv65ff%w&@a31zu26

    # db 환경변수
    MYSQL_ROOT_PASSWORD=vivadev
    MYSQL_DATABASE=vivadev
    MYSQL_USER=vivadev
    MYSQL_PASSWORD=vivadev

    # app 환경변수
    DATABASE_NAME=vivadev
    DATABASE_USER=vivadev
    DATABASE_PASSWORD=vivadev
    DATABASE_HOST=db
    DATABASE_PORT=3306
    ```


3. 도커 컴포즈로 컨테이너를 실행한다.
    - `docker compose up --build`

4. 실행중인 db 컨테이너에 들어가서 vivadev에게 모든 권한을 부여한다. 테스트 돌리려면 필요하다.

    - $ `docker compose exec -it db /bin/sh`
    - $ `mysql -u root -p`
    - $ `GRANT ALL PRIVILEGES ON 'test_vivadev'.* TO 'vivadev'@'%';`
    - $ `FLUSH PRIVILEGES;`
    - $ `SHOW GRANTS FOR 'vivadev'@'%';`


## 📍 디렉토리 구조
```
.
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── management
│   │   ├── __init__.py
│   │   └── commands
│   │       ├── __init__.py
│   │       └── wait_for_db.py
│   ├── migrations
│   ├── models.py
│   └── tests
│       ├── __init__.py
│       ├── test_commands.py
│       └── test_user_model.py
├── users
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── exceptions.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_user_api.py
│   ├── urls.py
│   ├── validators.py
│   └── views.py
├── posts
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── exceptions.py
│   ├── serializers.py
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_post_api.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```


## 📍 과제에 적용하고 싶었던 부분
- [ ] 레이어드 아키텍처 적용하기
- [X] API 문서화 스웨거 or 포스트맨 사용하기
- [X] TDD에 익숙해지기 위해 유닛테스트 작성 후, 코드 작성하기
- [ ] 인증 및 인가 미들웨어로 구현하기
- [ ] monggodb로 로그 수집하기
- [X] 도커 컴포즈로 환경 구축하기
- [X] DB는 mysql 연동하기
- [X] README.md 잘 작성하기 


## 📍 과제에 대한 회고
- 실무에서 Docker, Docker-compose, TDD를 경험해보지 못해서 최근에 공부중이었고, 이에 대한 부분을 꼭 적용해보고 싶었습니다.
- mysql은 오랜만에 사용하다보니 연동하는데 삽질도 많이 하고, 생각보다 시간이 많이 걸렸습니다.
- 대략 시간분배를 해두었는데, 예상치 못한 변수가 너무 많이 발생해서 계획대로 안된 점이 너무 아쉬웠습니다.
- DRF로 API를 개발할 때 viewset을 주로 사용하다가, DRF에 좀 더 효율적인 아키텍처에 대해 고민하게 되었습니다. 비즈니스 로직을 빼고, 레포지토리 패턴을 적용해보고 싶었는데 아직 학습이 더 필요한 단계라고 느꼈습니다.
- GenericAPIView으로 개발을 하면서 어떤 부분을 보완해야 하는지 알게 되었습니다.
- 이번 과제를 통해 역시 뭔가를 알고 모르고 판단하기 가장 좋은 방법은 직접 구현해 보는 것이라고 다시 한번 느꼈습니다. 앞으로 어떤 부분을 보완하면 좋을지 확실하게 알게 되어 좋았습니다.