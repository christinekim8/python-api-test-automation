@echo off
echo Starting WooCommerce API Automation Tests...
docker compose up --build --exit-code-from test-runner --abort-on-container-exit
echo Done!
echo Open allure-report/index.html in your browser to view the report.