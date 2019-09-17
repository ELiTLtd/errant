#!/bin/bash

pip3 install --target ./package -r app/requirements.txt
zip -r9 ${OLDPWD}/function.zip .
