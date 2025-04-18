from apps.users.tests.factories import UserFactory


def test_model(db):
    member = UserFactory.create()

    assert member.username
    assert member.avatar
    assert not member.avatar_thumbnail
