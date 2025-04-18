# 後台系統 - 後端服務

## 目錄
基於Django與Django REST framework開發的RESTful API Server

## 開發測試帳號
部分使用容器化的服務可以參考`docker-compose.yaml`中的設定

## 功能
- 會員 

### 功能細項


## 專案技術
其他技術細節請參考pyproject.toml，可以找到此專案的所有相關套件
- Django
- Django restframework
- celery
- flower
- PostgreSQL

## 指令集

### 指定本地python版本
如果需要追蹤專案有關的套件原始碼，會建議在本地指定好python版本後，使用poetry安裝並建立虛擬環境

[Modern Python Environment](https://testdriven.io/blog/python-environments/)
請參考pyenv的部分

[poetry document](https://python-poetry.org/docs/basic-usage/)，此部分作為reference，請執行以下指令
```bash
poetry install
poetry shell
```
就會啟動虛擬環境

### 啟動專案
環境變數請參考envs/.dev-sample
```bash
docker-compose up -d --build
```

### 專案命令行進入點，可以查詢有哪些命令
```
python manage.py --help
```

### 資料庫遷移相關指令

1. 進入容器
   ```bash
    docker-compose exec web bash
   ```
2. 修改models.py中，對應資料庫的欄位
3. 建立遷移腳本，請填入你對應的app-name
   ```bash
    python manage.py makemigrations <app-name>
    ```
4. 應用本次修改
   ```bash
    python manage.py migrate
    ```

### 創建超級用戶
 ```bash
python manage.py createsuperuser
 ```

### linter
```
make lint
```


### 測試相關
- 會使用pytest作為測試工具

## 環境變數設定
### 環境變數說明
```
DEBUG=1
SECRET_KEY=dbaa1_i7%*3r9-=z-+_mz4r-!qeed@(-a_r(g@k8jo8y3r27%m
DJANGO_ALLOWED_HOSTS=*

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=hello_django
SQL_USER=hello_django
SQL_PASSWORD=hello_django
SQL_HOST=db
SQL_PORT=5432

# Redis 設定
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=1

CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0

CHANNELS_REDIS=redis://redis:6379/0
```

## 資料夾說明
```
.
├── README.md                         # 專案說明文件，包含專案介紹、安裝步驟、使用方式等資訊。
├── apps                              # 主要應用程式目錄，包含不同的 Django 應用程式 (App)。
│   ├── __init__.py                   
│   ├── auth                          # 負責身份驗證 (Authentication) 的應用程式。
│   │   ├── __init__.py               
│   │   ├── admin.py                  # 註冊 `auth` 模組相關的 Model 到 Django Admin。
│   │   ├── apps.py                   # 定義 `auth` 應用程式的 Django 設定。
│   │   ├── migrations                # `auth` 應用程式的資料庫遷移 (Migrations) 目錄。
│   │   │   └── __init__.py           # 資料庫遷移初始化文件。
│   │   ├── models.py                 # 定義 `auth` 應用程式的資料庫模型 (User, Token等)。
│   │   ├── serializers.py            # 負責將 `auth` 相關的資料模型序列化為 JSON 格式。
│   │   ├── tests                     # `auth` 應用程式的測試目錄。
│   │   │   ├── __init__.py           
│   │   │   ├── test_models.py        # 測試 `auth` 模組的 Models。
│   │   │   ├── test_serializers.py   # 測試 `auth` 模組的 Serializers。
│   │   │   ├── test_views.py         # 測試 `auth` API。
│   │   │   ├── test_urls.py          # 測試 `auth` API 路由。
│   │   ├── urls.py                   # 定義 `auth` 應用程式的 API 路由。
│   │   └── views.py                  # 定義 `auth` 應用程式的 API 視圖 (Views)。
│   ├── users                         # 用戶管理 (User Management) 應用程式。
│   │   ├── __init__.py               # `users` 模組初始化文件。
│   │   ├── admin.py                  # 註冊 `users` 模組相關的 Model 到 Django Admin。
│   │   ├── apps.py                   # 定義 `users` 應用程式的 Django 設定。
│   │   ├── migrations                # `users` 應用程式的資料庫遷移 (Migrations) 目錄。
│   │   │   ├── 0001_initial.py       # 初始資料庫遷移檔案，建立 User 模型。
│   │   │   └── __init__.py           
│   │   ├── models.py                 # 定義 `users` 應用程式的資料庫模型 (User, Profile等)。
│   │   ├── serializers.py            # 負責將 `users` 相關的資料模型序列化為 JSON 格式。
│   │   ├── services.py               # 服務層，封裝與 `users` 相關的業務邏輯。
│   │   ├── tasks.py                  # `users` 應用程式的非同步任務 (Celery 任務)。
│   │   ├── tests                     # `users` 應用程式的測試目錄。
│   │   │   ├── __init__.py           
│   │   │   ├── test_models.py        # 測試 `users` 模組的 Models。
│   │   │   ├── test_serializers.py   # 測試 `users` 模組的 Serializers。
│   │   │   ├── test_services.py      # 測試 `users` 模組的 Services。
│   │   │   ├── test_views.py         # 測試 `users` API。
│   │   │   ├── test_urls.py          # 測試 `users` API 路由。
│   │   ├── urls.py                   # 定義 `users` 應用程式的 API 路由。
│   │   ├── validators.py             # 定義 `users` 相關的資料驗證 (e.g. 電子郵件格式、手機號碼驗證)。
│   │   └── views.py                  # 定義 `users` 應用程式的 API 視圖 (Views)。
├── core                              # 核心設定與專案入口。
│   ├── __init__.py                   
│   ├── asgi.py                       # ASGI 應用入口 (用於 Django Channels 或 FastAPI)。
│   ├── celery.py                     # Celery 設定檔，負責整合 Celery 任務管理。
│   ├── settings.py                   # Django 設定檔，包含資料庫、CORS、REST Framework、認證機制等設定。
│   ├── urls.py                       # 定義專案的主 API 路由。
│   ├── wsgi.py                       # WSGI 應用入口 (用於 Gunicorn 部署 Django)。
│   ├── tests                         # 全域測試目錄（適用於跨應用測試）。
│   │   ├── __init__.py          
│   │   ├── test_auth.py              # 測試認證機制。
│   │   ├── test_admin.py             # 測試 Django Admin。
│   │   ├── conftest.py               # pytest fixtures（共用測試資源）。
├── tests                             # 獨立於應用模組的測試目錄，包含 pytest 全域配置及跨模組測試。
│   ├── __init__.py              
│   ├── conftest.py                   # 全域 pytest fixture 設定。
│   ├── test_health_check.py          # 測試應用健康狀態 API。
│   ├── test_api_permissions.py       # 測試 API 權限管理。
│   ├── test_middleware.py            # 測試中介軟體 (Middleware)。
│   ├── test_throttling.py            # 測試 API 請求限制。
├── pytest.ini                        # pytest 設定檔，包含 Django 設定、測試發現規則、測試覆蓋率等。
├── requirements.txt                  # Python 依賴套件列表。
├── poetry.lock                       # Poetry 依賴鎖定檔案。
├── pyproject.toml                    # Poetry 設定檔，定義 Python 套件與相依性。
├── docker-compose.yaml               # Docker Compose 設定檔，定義專案的服務與依賴項 (e.g. PostgreSQL, Redis)。
└── utils                             # 通用工具函式目錄。
    ├── __init__.py                   
    ├── pagination.py                 # 自訂分頁功能，用於 Django REST Framework 的 API 分頁邏輯。
```



### 常用指令
- docker 常用指令
```angular2html
docker-compose ps  # 列出當前的服務
docker-compose up -d --build  # 啟動當前所有服務
docker-compose down -v  # 停止並移除所有服務，包含volume
```

## 第三方服務