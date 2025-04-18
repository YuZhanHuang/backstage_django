import os
from io import BytesIO

from PIL import Image
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

User = get_user_model()


@shared_task(name="task_clear_session")
def task_clear_session():
    from django.core.management import call_command

    call_command("clearsessions")


@shared_task(name='generate_avatar_thumbnail')
def generate_avatar_thumbnail(user_pk):
    try:
        user = User.objects.get(pk=user_pk)
        if not user.avatar:
            return

        im = Image.open(user.avatar)
        if im.mode == "RGBA":
            im = im.convert("RGB")

        # 產生縮圖
        size = (100, 100)
        im.thumbnail(size)
        thumb_io = BytesIO()
        im.save(thumb_io, format='JPEG')

        avatar_name = os.path.basename(user.avatar.name)
        thumbnail_name = avatar_name.replace(".", "-thumbnail.")  # 例: abc123-thumbnail.jpg

        user.avatar_thumbnail.save(
            f"{thumbnail_name}",
            ContentFile(thumb_io.getvalue()),
            save=True
        )

    except User.DoesNotExist:
        print(f"User with ID {user_pk} not found.")
    except Exception as e:
        print(f"Error generating avatar thumbnail: {str(e)}")
