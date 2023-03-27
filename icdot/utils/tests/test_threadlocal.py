from icdot.utils import threadlocal


def test_default_user_value_is_none():
    user = "foo"
    threadlocal.set_current_user(user)
    assert threadlocal.get_current_user() is user
    threadlocal.clear()
    assert threadlocal.get_current_user() is None


def test_setting_user():
    for user in ("foo", "bar", None, 1):
        threadlocal.set_current_user(user)
        assert threadlocal.get_current_user() is user


def test_context_manager():
    threadlocal.set_current_user("previous")
    previous = threadlocal.get_current_user()
    new = "foo"

    with threadlocal.current_user(new) as user:
        assert user is new
        assert threadlocal.get_current_user() is new

    assert threadlocal.get_current_user() is previous


def test_context_manager_handling_exception():
    threadlocal.set_current_user("previous")
    previous = threadlocal.get_current_user()
    new = "foo"

    try:
        with threadlocal.current_user(new) as user:
            assert user is new
            assert threadlocal.get_current_user() is new
            raise RuntimeError()
    except RuntimeError:
        pass  # We just wanted to abort the context.

    assert threadlocal.get_current_user() is previous
