#!/usr/bin/env sh
set -eu
envsubst '${PROXYPASS}' < /etc/nginx/sites-enabled/mlflow.conf.template > /etc/nginx/sites-enabled/mlflow.conf
exec "$@"