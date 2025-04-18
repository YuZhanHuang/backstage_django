.PHONY: lint format check test

# 🔍 代碼檢查 (Linter)
.PHONY: lint format check test

# 🔍 代碼檢查 (Linter)
lint:
	poetry run flake8 . || true
	poetry run black --check . || true
	poetry run isort --check . || true
	poetry run pylint $(git ls-files '*.py') || true
	poetry run mypy . || true


# 🛠 代碼格式化
format:
	poetry run black .
	poetry run isort .

# ✅ 檢查格式但不修改
check:
	poetry run black --check .
	poetry run isort --check .


