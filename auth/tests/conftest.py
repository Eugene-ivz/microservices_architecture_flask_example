import pytest

from app.extensions import db as _db
from app.hashing import get_password_hash
from app.main import create_app
from app.models import User


@pytest.fixture(scope="session")
def app():
    '''
    app fixture created from flask factory pattern function with test configuration
    
    '''
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql+psycopg://postgres:postgres@localhost:5556/test_users",
        "JWT_COOKIE_CSRF_PROTECT": False,
    }
    _app = create_app(test_config)

    with _app.app_context():
        yield _app


@pytest.fixture(scope="function")
def client(app):
    '''
    flask test client
      
    '''
    yield app.test_client(use_cookies=True)


@pytest.fixture(scope="session")
def db(app, request):
    '''
    session scoped database
    
    '''
    def teardown():
        _db.drop_all()

    _db.app = app

    _db.create_all()
    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
def user():
    '''
    user fixture
    
    '''
    user = User(
        username="test1", password=get_password_hash("test1"), email="test1@t.com"
    )
    return user


@pytest.fixture(scope="function")
def session(db, request, user):
    '''
    function scoped database connection
    which rollsback at the end of the test
    '''
    db.session.begin_nested()

    def commit():
        db.session.flush()

    old_commit = db.session.commit
    db.session.commit = commit

    db.session.add(user)
    db.session.commit()

    def teardown():
        db.session.rollback()
        db.session.close()
        db.session.commit = old_commit

    request.addfinalizer(teardown)
    return db.session
