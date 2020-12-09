#!/bin/sh
tar -c -f device_layer.tar "../source/device_manager/device_layer"
docker build -t user_script .
