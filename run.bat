@echo off
echo Starting WooCommerce API Automation Tests...
docker compose up --build -d
docker wait woo-test-runner
docker logs woo-test-runner
docker compose down
echo Done!
echo Opening Allure Report...
start allure-report\index.html