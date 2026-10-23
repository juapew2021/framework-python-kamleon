.PHONY: test smoke sanity report full clean

clean:
	rm -rf reports/allure-results
	rm -rf reports/allure-report

test:
	pytest -v --alluredir=reports/allure-results

smoke:
	pytest -v -m smoke --alluredir=reports/allure-results

sanity:
	pytest -v -m sanity --alluredir=reports/allure-results

report:
	allure serve reports/allure-results

full:
	pytest -v --alluredir=reports/allure-results
	allure generate reports/allure-results -o reports/allure-report --clean
	allure open reports/allure-report