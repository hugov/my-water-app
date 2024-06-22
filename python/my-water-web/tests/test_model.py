import pytest
import model
import main

@pytest.fixture
def app():
    app = main.CreateApp()
    with app.app_context():
        yield app

@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield

@pytest.mark.usefixtures("app_ctx")
def test_consultarContaBancaria():
    conta = model.consultarContaBancaria(1)
    assert conta.id == 1
