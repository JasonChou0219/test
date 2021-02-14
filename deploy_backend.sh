#!/bin/bash
INSTALL_DIR=/usr/device-manager
CONFIG_DIR=/etc/device-manager
export DEVICE_MANAGER_ENV_PRODUCTION=1
if [ ! -d ${CONFIG_DIR} ]
then
	mkdir ${CONFIG_DIR}
	python3 generate_config.py
fi

if [ -d ${INSTALL_DIR} ]
then
	rm -rf ${INSTALL_DIR}
fi
mkdir ${INSTALL_DIR}
mkdir ${INSTALL_DIR}/.venv

cp Pipfile ${INSTALL_DIR}
cp Pipfile.lock ${INSTALL_DIR}

cp backend.py ${INSTALL_DIR}
cp backend.sh ${INSTALL_DIR}
cp scheduler.py ${INSTALL_DIR}
cp scheduler.sh ${INSTALL_DIR}
cp replace_files.py ${INSTALL_DIR}

cp -r source ${INSTALL_DIR}
cp -r user_script_env ${INSTALL_DIR}
cp -r .venv/ ${INSTALL_DIR}
