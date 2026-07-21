from history import is_new_project


def test_new_project_returns_true():
    history = {"123", "456"}

    assert is_new_project("789", history)


def test_existing_project_returns_false():
    history = {"123", "456"}

    assert not is_new_project("123", history)
