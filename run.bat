@echo off
echo Starting WooCommerce API Automation Tests...
docker compose up --build --abort-on-container-exit --exit-code-from test-runner
echo Done!