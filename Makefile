include env

build:
	docker compose build

up:
	docker compose --env-file env up -d

down:
	docker compose --env-file env down

restart:
	make down && make up

to_minio:
	docker exec -it minio_vnexpress mc ls minio/vnexpress
