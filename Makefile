path := .

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: lint
lint: black isort flake mypy	## Apply all the linters

.PHONY: clean
clean: 	## Clean pycache remove folder lo
	@echo
	@echo "Clean pycache..."
	@echo "================="
	@echo
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d | xargs rm -fr

.PHONY: clean-all
clean-all: 	## Clean pycache and folders logs
	@echo
	@echo "Clean pycache and logs..."
	@echo "================="
	@echo
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d | xargs rm -fr
	@rm -fr logs/
	@rm -fr Saida/


.PHONY: lint-check
lint-check: ## Aplica a limpeza geral
	@echo
	@echo "Checking linter rules..."
	@echo "========================"
	@echo
	@black --check $(path)
	@isort --check $(path)
	@flake8 $(path)
	@mypy $(path)


.PHONY: black
black: ## Apply black
	@echo
	@echo "Applying black..."
	@echo "================="
	@echo
	@ # --fast was added to circumnavigate a black bug
	@black --fast $(path)
	@echo


.PHONY: isort
isort: ## Apply isort
	@echo "Applying isort..."
	@echo "================="
	@echo
	@isort $(path)


.PHONY: flake
flake: ## Apply flake8
	@echo
	@echo "Applying flake8..."
	@echo "================="
	@echo
	@flake8 $(path)


.PHONY: mypy
mypy: ## Apply mypy
	@echo
	@echo "Applying mypy..."
	@echo "================="
	@echo
	@mypy $(path)


.PHONY: trim-imports
trim-imports: ## Remove unused imports
	@autoflake --remove-all-unused-imports \
	--ignore-init-module-imports \
	--in-place \
	--recursive \
	$(path)


.PHONY: show_packages
show_packages: ## Show all installed packages
	poetry show


.PHONY: show_latest_packages
show_latest_packages: ## Compare installed packages with new site version
	poetry show --latest

.PHONY: check
check: ## Pre-commit Check all Files
	pre-commit run --all-files

.PHONY: req
req: ## Show many infos
	poetry env info --path
	poetry show --tree
	poetry check
	poetry export -f requirements.txt --without-hashes  > requirements.txt
	cat requirements.txt

.PHONY: update
update: ## Update Poetry Version
	poetry update
	@$(MAKE) -f $(THIS_MAKEFILE) req
	git diff requirements.txt
	pre-commit autoupdate

.PHONY: venv
venv: ## Executeo poetry shell
	poetry shell

.PHONY: install
install: ## Poetry Install packages
	poetry install
	@$(MAKE) venv

.PHONY: updatetools
updatetools: ## Update Pre-commit
	pre-commit autoupdate
