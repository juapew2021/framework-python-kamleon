#!/bin/bash

export PATH="/opt/homebrew/bin:$PATH"

# Uso: ./run_qa.sh [regression|smoke|sanity]   (por defecto: regression)
SUITE="${1:-regression}"

case "$SUITE" in
  smoke)      MARK_ARGS="-m smoke" ;;
  sanity)     MARK_ARGS="-m sanity" ;;
  regression) MARK_ARGS="" ;;
  *) echo "Suite desconocida: $SUITE (usa regression, smoke o sanity)"; exit 1 ;;
esac

echo "Ejecutando suite: $SUITE"

pytest -v --alluredir=reports/allure-results $MARK_ARGS

allure generate \
reports/allure-results \
-o reports/allure-report \
--clean

allure open reports/allure-report