from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.rbac.models import Role, Permission

User = get_user_model()


class Command(BaseCommand):
    help = "Initialize RBAC data (roles, permissions, and users)"

    def handle(self, *args, **kwargs):
        self.stdout.write("📌 Inserting initial RBAC data...")

        # 🔹 **確保 Joe 存在，並設定為 `created_by` & `updated_by`**
        joe, _ = User.objects.get_or_create(
            username="Joe",
            defaults={"email": "joe@example.com", "is_staff": True, "is_active": True}
        )
        joe.set_password("Test1234")
        joe.save()

        # 🔹 **建立文章 (Article) 的 CRUD 權限**
        perm_article_create, _ = Permission.objects.get_or_create(code='article:create', defaults={
            'description': '新增文章', 'category': '文章管理', 'created_by': joe, 'updated_by': joe})
        perm_article_read, _ = Permission.objects.get_or_create(code='article:read', defaults={
            'description': '閱讀文章', 'category': '文章管理', 'created_by': joe, 'updated_by': joe})
        perm_article_update, _ = Permission.objects.get_or_create(code='article:update', defaults={
            'description': '修改文章', 'category': '文章管理', 'created_by': joe, 'updated_by': joe})
        perm_article_delete, _ = Permission.objects.get_or_create(code='article:delete', defaults={
            'description': '刪除文章', 'category': '文章管理', 'created_by': joe, 'updated_by': joe})

        # 🔹 **建立角色**
        admin_role, _ = Role.objects.get_or_create(name='Admin',
                                                   defaults={'level': 1, 'created_by': joe, 'updated_by': joe})
        manager_role, _ = Role.objects.get_or_create(name='Manager',
                                                     defaults={'level': 2, 'created_by': joe, 'updated_by': joe})
        senior_role, _ = Role.objects.get_or_create(name='Senior',
                                                    defaults={'level': 3, 'created_by': joe, 'updated_by': joe})
        junior_role, _ = Role.objects.get_or_create(name='Junior',
                                                    defaults={'level': 4, 'created_by': joe, 'updated_by': joe})

        # 🔹 **分配權限**
        admin_role.permissions.set([
            perm_article_create, perm_article_read, perm_article_update, perm_article_delete
        ])
        manager_role.permissions.set([
            perm_article_create, perm_article_read, perm_article_update
        ])
        senior_role.permissions.set([
            perm_article_create, perm_article_read, perm_article_update
        ])
        junior_role.permissions.set([
            perm_article_read
        ])

        # 🔹 **建立其他使用者並設定角色**
        users_data = [
            {"username": "Riz111", "email": "riz111@example.com", "roles": [manager_role]},
            {"username": "Peter111", "email": "peter111@example.com", "roles": [senior_role]},
            {"username": "Terry111", "email": "terry111@example.com", "roles": [senior_role]},
            {"username": "John111", "email": "john111@example.com", "roles": [senior_role]},
            {"username": "Alex111", "email": "alex111@example.com", "roles": [junior_role]},
        ]

        for user_data in users_data:
            user, _ = User.objects.get_or_create(
                username=user_data["username"],
                created_by=joe,
                updated_by=joe,
                defaults={"email": user_data["email"], "is_active": True}
            )
            user.set_password("Test1234")
            user.roles.set(user_data["roles"])
            user.save()

        self.stdout.write(self.style.SUCCESS("✅ RBAC initial data inserted successfully."))
