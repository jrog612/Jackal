#! /bin/bash

clear()
{
    if [[ -d build ]]; then rm -r build
    fi

    if [[ -d dist ]]; then rm -r dist
    fi

    if [[ -d django_jackal.egg-info ]]; then rm -r django_jackal.egg-info
    fi
}

clear
python setup.py sdist bdist_wheel
twine upload -r pypitest dist/*
clear