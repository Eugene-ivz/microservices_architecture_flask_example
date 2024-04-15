from sqlalchemy import select

from app.models import User


def test_create_delete_user(session):
    user = User(username="test", password="test")
    session.add(user)
    session.commit()
    assert user == session.scalar(select(User).where(User.username == user.username))
    assert (
        user.password
        == session.scalar(select(User).where(User.username == user.username)).password
    )
    session.delete(user)
    session.commit()
    assert user not in session.scalars(select(User)).all()


def test_existing_user(session):

    user = User(username="test1", password="test1")
    assert (
        user.username
        == session.scalar(select(User).where(User.username == user.username)).username
    )
