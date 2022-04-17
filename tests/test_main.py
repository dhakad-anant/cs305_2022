from pkg.main import Main
from pkg.main import run

def test_singleFile():
    obj = Main('tests/testImages/cleancode.png', '-file', ['en'], False)
    assert len(obj.execute()) == 1

def test_directory():
    obj = Main('tests/testImages/', '-dir', ['en'], False)
    assert len(obj.execute()) == 7

def test_run():
    assert run(['main.py', '-file', 'tests/testImages/cleancode.png']) == True