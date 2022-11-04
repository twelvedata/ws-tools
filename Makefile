PATH_THIS:=$(realpath $(dir $(lastword ${MAKEFILE_LIST})))

help:
	@echo "    dev"
	@echo "        Initialise virtualenv with dev requirements"
	@echo "    subscription-monitoring"
	@echo "        Run monitoring of subscription"


.PHONY: dev
dev:
	python3 -m venv venv
	PYTHONPATH=$$PYTHONPATH:`realpath $(PATH_THIS)` \
	&& printf '#!/bin/bash\n%s/venv/bin/pip3 "$$@"' $(PATH_THIS) > $(PATH_THIS)/pip3 \
	&& printf '#!/bin/bash\n%s/venv/bin/python3 "$$@"' $(PATH_THIS) > $(PATH_THIS)/python3 \
	&& chmod +x $(PATH_THIS)/pip3 \
	&& chmod +x $(PATH_THIS)/python3 \
	&& $(PATH_THIS)/pip3 install --upgrade pip \
	&& $(PATH_THIS)/pip3 install -Ur $(PATH_THIS)/requirements-dev.txt \
	&& $(PATH_THIS)/pip3 install -Ur $(PATH_THIS)/requirements.txt

.PHONY: dev-run
dev-run:
	PYTHONPATH=$$PYTHONPATH:`realpath $(PATH_THIS)` \
	&& export PYTHONPATH \
	&& $(PATH_THIS)/python3 $(command)

.PHONY: subscription-monitoring
subscription-monitoring:
	$(PATH_THIS)/venv/bin/watchmedo auto-restart -p '*.py' --recursive -- \
	make dev-run command="subscription-monitoring.py"

.PHONY: delay-monitoring
delay-monitoring:
	$(PATH_THIS)/venv/bin/watchmedo auto-restart -p '*.py' --recursive -- \
	make dev-run command="delay-monitoring.py"
