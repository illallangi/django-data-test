.PHONY: usage
usage:
	@echo "Usage: make [target]"
	@echo
	@echo "Targets:"
	@echo "  clean       Remove all generated files"
	@echo "  lint        Run ruff format, check and uv sync"
	@echo "  commit      Run cz commit"
	@echo "  build       Build the project"
	@echo "  image       Build an image"
	@echo
	@echo "  migrate     Run django migrate"
	@echo "  sync        Run django sync"
	@echo "  serve       Run django runserver"
	@echo

.PHONY: clean
clean:
	@git clean -Xdf
	@mkdir -p .git/hooks
	@rm -f .git/hooks/*.sample
	@find .git/hooks/ -type f  | while read i; do chmod +x $$i; done

.PHONY: lint
lint:
	@uv run --quiet deptry src --experimental-namespace-package
	@uv run --quiet ruff format src
	@uv run --quiet djlint --reformat src --quiet || true
	@uv run --quiet ruff check src --quiet
	@uv run --quiet djlint --lint src --quiet
	@uv sync --quiet

.PHONY: commit
commit: lint
	@uv run --quiet cz commit

.PHONY: build
build: lint
	@uv build

.PHONY: image
image: build
	@podman build --format=docker --tag illallangi-data:latest .

.PHONY: runimage
runimage: image
	@fuser --kill 58000/tcp || true
	@podman run \
		-it \
		--rm \
		-e DJANGO_SECRET_KEY=$$(uv run python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())') \
		-e DATA_PLUGIN_AIR_TRANSPORT="illallangi-data-air-transport>=0.4.1" \
		-e DATA_PLUGIN_AVIATION="illallangi-data-aviation>=0.4.0" \
		-e DATA_PLUGIN_EDUCATION="illallangi-data-education>=0.3.0" \
		-e DATA_PLUGIN_FITNESS="illallangi-data-fitness>=0.5.0" \
		-e DATA_PLUGIN_MASTODON="illallangi-data-mastodon>=0.5.0" \
		-e DATA_PLUGIN_RESIDENTIAL="illallangi-data-residential>=0.3.0" \
		-e DATA_PORT=58000 \
		-v $${HOME}/.config:/config/.cache:rw \
		--env-file $$(uv run python -c "from dotenv import find_dotenv; print(find_dotenv())") \
		-p 58000:58000 \
		illallangi-data:latest

.PHONY: check
check: lint
	@DATA_CONFIG_DIR=$$(pwd) uv run src/manage.py check --fail-level=WARNING

.PHONY: migrate
migrate: check lint
	@mkdir -p src/illallangi/django/data/static
	@DATA_CONFIG_DIR=$$(pwd) uv run src/manage.py migrate
	@DATA_CONFIG_DIR=$$(pwd) uv run src/manage.py createsuperuserwithpassword --username admin --email me@example.com --password admin --preserve

.PHONY: sync
sync: synchronize

.PHONY: synchronise
synchronise: synchronize

.PHONY: synchronize
synchronize: migrate check lint
	@DATA_CONFIG_DIR=$$(pwd) uv run src/manage.py synchronize

.PHONY: serve
serve: sync migrate check lint
	@DATA_CONFIG_DIR=$$(pwd) uv run src/manage.py runserver 0.0.0.0:58000
