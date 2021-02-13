#!/bin/bash
INSTALL_DIR=/device-manager
CONFIG_DIR=/etc/device-manager
export DEVICE_MANAGER_ENV_PRODUCTION=1
if [ ! -d ${CONFIG_DIR} ]
then
	mkdir ${CONFIG_DIR}
fi

if [ ! -d ${INSTALL_DIR} ]
then
	mkdir ${INSTALL_DIR}
fi

cp backend.py ${INSTALL_DIR}
cp scheduler.py ${INSTALL_DIR}
cp -r ./source ${INSTALL_DIR}
cp -r ./user_script_env ${INSTALL_DIR}
python3 generate_config.py
python3 setup_test_db.py
docker build -t user_script ./user_script_env/

