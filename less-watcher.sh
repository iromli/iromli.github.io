#!/usr/bin/env sh
watchmedo shell-command \
    --patterns="*.less" \
    --recursive \
    --command="lessc -x $PWD/less/style.less > $PWD/theme/css/style.css" \
    $PWD
