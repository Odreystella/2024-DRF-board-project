from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check):
        """
        데이터베이스가 준비되었다는 걸 확인하는 테스트.
        """
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check): # @추가되면 안쪽부터 파라미터로 넣어줌
        """
        OperationalError 발생했을 때, 데이터베이스가 기다리는지 확인하는 테스트.
        """
        patched_check.side_effect = [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 4)
        patched_check.assert_called_with(databases=['default'])