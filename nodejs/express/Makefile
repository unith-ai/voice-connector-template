.PHONY: all
all: help

.PHONY: help
help:
	@echo '----'
	@echo 'build                 - build docker image for production'
	@echo 'run                   - run the docker container previously built'

.PHONY: build
build:
	docker build . --target builder -t express-connector:0.0.1

.PHONY: run
run:
	docker run -e unithApiKey=12345678 -it -p 8080:8080 --rm express-connector:0.0.1