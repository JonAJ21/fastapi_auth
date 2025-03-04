DC = docker-compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
DOCKER_COMPOSE_FILE = docker-compose.yaml
AUTH_CONTAINER = auth-service
BOT_CONTAINER = bot

.PHONY: app
app:
	${DC} -f ${DOCKER_COMPOSE_FILE} ${ENV} up --build -d

.PHONY: app-up
app-up:
	${DC} -f ${DOCKER_COMPOSE_FILE} ${ENV} up -d

.PHONY: app-down
app-down:
	${DC} -f ${DOCKER_COMPOSE_FILE} down

.PHONY: auth-shell
auth-shell:
	${EXEC} ${AUTH_CONTAINER} bash

.PHONY: auth-logs
auth-logs:
	${LOGS} ${AUTH_CONTAINER} -f

.PHONY: bot-shell
bot-shell:
	${EXEC} ${BOT_CONTAINER} bash

.PHONY: bot-logs
bot-logs:
	${LOGS} ${BOT_CONTAINER} -f