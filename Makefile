# Variabelen
DOCKER_IMAGE_NAME = $(shell basename $(CURDIR))
DOCKER_TAG = latest
RUNTIME_PATH = $(PWD)/.runtime

# Targets

## build: Bouwt de Docker container.
build:
	@docker build -f Dockerfile -t $(DOCKER_IMAGE_NAME):$(DOCKER_TAG) .
	@echo "Docker image $(DOCKER_IMAGE_NAME):$(DOCKER_TAG) is built."
	echo
	@echo "Available alias for this container: 'çontainer'"

## run: Draait de Docker container.
run:
	@docker run -it --rm $(DOCKER_IMAGE_NAME):$(DOCKER_TAG)

## shell: Start een shell in de Docker container.
shell:
	@docker run -it --rm $(DOCKER_IMAGE_NAME):$(DOCKER_TAG) /bin/sh

## clean: Verwijdert de Docker container en image.
clean:
	@docker rmi -f $(DOCKER_IMAGE_NAME):$(DOCKER_TAG)

## help: Toont deze hulptekst.
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
