#! /bin/bash

set -euo pipefail
trap 's=$?; echo >&2 "$0: Error on line "$LINENO": $BASH_COMMAND"; exit $s' ERR

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

pushd "$SCRIPT_DIR" || {
    printf "Unable to cd int the target directory!\n"
    exit 1
}

if [[ (! -d './env') || (! -f './env/bin/activate') ]]; then
    python -m venv env
fi

source './env/bin/activate'
pip install -r dev_requirements.txt
deactivate || true

popd || {
    printf "Unable to cd to the starting directory!\n"
    exit 1
}
