# 2024-DRF-board-project

## 🌈 설치 및 실행 방법
1. `.env` 파일 추가한다.
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


2. `docker compose up --build` 명령을 실행한다.

3. 실행중인 db 컨테이너에 들어가서 vivadev에게 모든 권한을 부여한다. 테스트 돌리려면 필요하다.

- $ `docker compose exec -it db /bin/sh`
- $ `mysql -u root -p`
- $ `GRANT ALL PRIVILEGES ON `test_vivadev`.* TO 'vivadev'@'%';`
- $ `FLUSH PRIVILEGES;`
- $ `SHOW GRANTS FOR 'vivadev'@'%';`