# Makefile for LLM Advanced Testing Suite

.PHONY: help install install-dev install-optional test test-coverage test-unit test-integration lint format type-check security-check build clean docs serve-docs release deploy

help:  ## Show this help message
	@echo "LLM Advanced Testing Suite Development Commands:"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "%-20s %s\n", "Target", "Description"} /^[a-zA-Z_-]+:.*?##/ { printf "%-20s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install:  ## Install dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

install-optional:  ## Install optional dependencies
	pip install -r requirements-optional.txt

test:  ## Run all tests
	pytest

test-coverage:  ## Run tests with coverage
	pytest --cov=. --cov-report=html --cov-report=term-missing

test-unit:  ## Run unit tests
	pytest -m unit

test-integration:  ## Run integration tests
	pytest -m integration

test-fast:  ## Run tests without coverage
	pytest --no-cov

lint:  ## Run linting
	flake8 . --max-line-length=88 --extend-ignore=E203,W503
	black --check . --line-length=88
	isort --check-only --profile=black --line-length=88

format:  ## Format code
	black . --line-length=88
	isort --profile=black --line-length=88

type-check:  ## Run type checking
	mypy . --ignore-missing-imports --strict-optional --no-strict-optional --warn-redundant-casts --warn-unused-ignores --warn-no-return --warn-unreachable --strict-equality

security-check:  ## Run security checks
	bandit -r .
	safety check

build:  ## Build package
	python -m build

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:  ## Build documentation
	cd docs && make html

serve-docs:  ## Serve documentation locally
	cd docs/build/html && python -m http.server 8000

release:  ## Create release
	@echo "Creating release..."
	@echo "Please ensure:"
	@echo "1. All tests are passing"
	@echo "2. Documentation is updated"
	@echo "3. Version is updated in pyproject.toml"
	@echo "4. Changelog is updated"
	@read -p "Press Enter to continue or Ctrl+C to abort..."
	python -m build
	twine upload dist/*

deploy:  ## Deploy to production
	@echo "Deploying to production..."
	@echo "Please ensure:"
	@echo "1. All tests are passing"
	@echo "2. Documentation is built"
	@echo "3. Docker image is built"
	@read -p "Press Enter to continue or Ctrl+C to abort..."
	docker build -t llmtest24:latest .
	docker push llmtest24:latest

docker-build:  ## Build Docker image
	docker build -t llmtest24:latest .

docker-run:  ## Run Docker container
	docker run -p 8501:8501 -v $(PWD)/testout:/app/testout -v $(PWD)/results:/app/results llmtest24:latest

docker-compose-up:  ## Start Docker Compose
	docker-compose up -d

docker-compose-down:  ## Stop Docker Compose
	docker-compose down

setup:  ## Initial setup
	python install.py
	pre-commit install

check:  ## Run all checks
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) security-check
	$(MAKE) test

ci:  ## Run CI checks locally
	$(MAKE) check
	$(MAKE) test-coverage

all:  ## Run all checks and tests
	$(MAKE) check
	$(MAKE) test-coverage
	$(MAKE) docs
