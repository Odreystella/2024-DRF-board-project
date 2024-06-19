import time

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Database가 연결 가능한 상태인지 확인하는 커스텀 커맨드.
    """
    help = 'Check if database is available'

    def handle(self, *args, **options):
        self.stdout.write('데이터베이스 기다리는 중...')
        db_up = False

        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except OperationalError:
                self.stdout.write('데이터베이스가 아직 준비되지 않았습니다. 잠시만 기다려주세요...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('데이터베이스 준비 완료!'))