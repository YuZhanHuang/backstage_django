from ..tasks import generate_avatar_thumbnail


def test_task_generate_avatar_thumbnail(db, user):
    # init state
    assert user.avatar
    assert not user.avatar_thumbnail

    generate_avatar_thumbnail(user.pk)

    user.refresh_from_db()

    assert user.avatar_thumbnail
    assert user.avatar_thumbnail.height == 100
    assert user.avatar_thumbnail.width == 100
