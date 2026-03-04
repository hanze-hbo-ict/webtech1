#!/usr/bin/env bash
branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$branch" = "main" ]; then
    echo "GEBLOKKEERD: commit nooit direct op main. Maak een feature branch."
    exit 1
fi
