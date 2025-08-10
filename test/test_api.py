def test_post_hero(test_app):
    """Тест успешной записи героя"""
    response = test_app.post("hero", params={"name": "test hero"})
    assert response.status_code == 201


def test_post_hero_unsuccessfully(test_app, mock_db):
    """Тест неуспешного добавления героя - такой герой уже существует"""
    method_check_hero = getattr(mock_db, "check_hero")
    method_check_hero.return_value = True

    response = test_app.post("hero", params={"name": "test hero"})
    assert response.status_code == 409


def test_get_hero(test_app):
    """Тест успешного получения списка героев"""
    result = test_app.get("hero")
    assert result.status_code == 200
    result = result.json()
    assert isinstance(result, list)
    assert len(result) > 0


def test_get_hero_unsuccessfully(test_app, mock_db):
    """Тест неуспешного получения героев - герои отсутствуют"""
    method_get_hero = getattr(mock_db, "get_hero")
    method_get_hero.return_value = []

    response = test_app.get("hero")
    assert response.status_code == 404
