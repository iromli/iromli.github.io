#!/usr/bin/env bash

# For some reasons, `mynt serve` command raises error,
# let's use another command.
if [[ ! -z `which mynt` ]]; then
    `mynt gen -f _build`
else
    echo ""
    echo "Unable to find 'mynt' executable."
    echo ""
    echo "    [sudo] pip install mynt"
    echo ""
fi
