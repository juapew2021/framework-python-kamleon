#!/bin/bash

export PATH="/opt/homebrew/bin:$PATH"

pytest -v --alluredir=reports/allure-results

allure generate \
reports/allure-results \
-o reports/allure-report \
--clean

allure open reports/allure-report