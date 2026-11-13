import time

import pytest

from python_drills.timer import Timer


def test_timer(capsys):
    with Timer("sleep") as t:
        time.sleep(0.1)
    assert 0.1 <= t.elapsed < 1
    captured = capsys.readouterr()
    assert t.label in captured.out


def test_timer_reports_error(capsys):
    with pytest.raises(ValueError), Timer("error") as t:
        raise ValueError()
    captured = capsys.readouterr()
    assert t.label in captured.out
