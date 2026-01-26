.PHONY: test test-up test-down

TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/test_db

test-up:
	docker run --rm -d --name pg-test -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=test_db -p 5433:5432 postgres:16

test:
	TEST_DATABASE_URL="$(TEST_DATABASE_URL)" pytest -q

test-down:
	docker stop pg-test || true