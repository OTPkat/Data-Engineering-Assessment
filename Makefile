DOCKER_COMP = DOCKER_BUILDKIT=1 docker-compose
DOCKER_COMP_F = $(DOCKER_COMP) -f docker-compose.yaml
.DEFAULT_GOAL = help
.PHONY        = help

## —————————— 🎵 Commands 🎵 ————————————————————————————————

up: ## Start database
	$(DOCKER_COMP_F) up -d database
build: ## Build
	$(DOCKER_COMP_F) build database
up-with-build: build up ## Build & Start database
up-no-build: up # Start containers without building
down: ## Stop containers
	$(DOCKER_COMP_F) down


## —————————— 🎵 Loader 🎵 —————————————————————————————
build-loader:
	$(DOCKER_COMP_F) build loader
load: up-no-build
	$(DOCKER_COMP) run loader
load-with-build: build-loader up-with-build
	$(DOCKER_COMP) run loader


## —————————— 🎵 Tester 🎵 —————————————————————————————
build-tester:
	$(DOCKER_COMP_F) build tester

test: up-no-build
	$(DOCKER_COMP) run -v ./data:/app/data tester

test-with-build: build-tester up-with-build
	$(DOCKER_COMP) run -v ./data:/app/data tester


## —————————— 🎵 Misc 🎵 —————————————————————————————
help: ## Outputs this help screen
	@grep -E '(^[a-zA-Z0-9_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | sed -E 's/(\.dev\.ignore\/)?Makefile?\://' |  awk 'BEGIN {FS = ":.*?## "}{printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'
query: ## Query
	$(DOCKER_COMP) exec -it database psql -U test_user -d test_db

log: ## Show Logs
	tail -n 100 -f $(PWD)/logs/*.log | awk '\
		{matched=0}\
		/INFO:/    {matched=1; print "\033[0;37m" $$0 "\033[0m"}\
		/WARNING:/ {matched=1; print "\033[0;34m" $$0 "\033[0m"}\
		/ERROR:/   {matched=1; print "\033[0;31m" $$0 "\033[0m"}\
		/Next/     {matched=1; print "\033[0;31m" $$0 "\033[0m"}\
		/ALERT:/   {matched=1; print "\033[0;35m" $$0 "\033[0m"}\
		/Stack trace:/ {matched=1; print "\033[0;35m" $$0 "\033[0m"}\
		matched==0            {print "\033[0;33m" $$0 "\033[0m"}\