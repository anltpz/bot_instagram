VENV="instagram_env"
virtual_env:
	python3 -m venv $(VENV)
	. ${VENV}/bin/activate


install:
	make virtual_env
	python3 -m pip install  --upgrade pip
	@pip3 install -r requirements.txt	

	@make env_activate


env_activate:
	@echo ">>>>>>>>>>>>>>>>>> ccalıs <<<<<<<<<<<<<<<<<<<<<<<<"

run:
	@python3  main.py

list:
	@pip3 list

leave:
	@deactivate
 