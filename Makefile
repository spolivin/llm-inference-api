build-base:
	docker build -f Dockerfile.base -t mybase:torch .

build-services:
	docker compose build

up-services:
	docker compose up -d

down-services:
	docker compose down --volumes --remove-orphans

remove-dangling:
	docker images -f "dangling=true" -q | xargs -r docker rmi

images:
	docker image ls

containers:
	docker ps -a

services:
	docker compose ls

open-ports:
	lsof -i -P -n | grep LISTEN

gpu:
	nvidia-smi

track-gpu:
	watch -n 1 nvidia-smi

format-code:
	isort . && black .
