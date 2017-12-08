#!/bin/bash

VIRTUAL_ENV=.venv

INSTALL_DEPS="no"
if [ ! -d ${VIRTUAL_ENV} ]; then
	virtualenv ${VIRTUAL_ENV} -p `which python3`
	INSTALL_DEPS="yes"
fi

source ${VIRTUAL_ENV}/bin/activate

if [ "${INSTALL_DEPS}" == "yes" ]; then
	pip install -r tools/requirements.txt
fi

ROOT_DIR=`pwd`

for DIRECTORY_NAME in `find  -mindepth 1 -type d| grep -v tools | grep -v .git | grep -v .venv`
do
	DIRECTORY_TO_PROCESS="${DIRECTORY_NAME:2}"
	echo "Found directory: ${DIRECTORY_TO_PROCESS}"
	pushd "${DIRECTORY_TO_PROCESS}"
		python ${ROOT_DIR}/tools/validate.py
	popd
done
