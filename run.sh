#!/bin/bash
echo "🚀 Starting WooCommerce API Automation Tests..."
docker compose up --build -d
docker wait woo-test-runner
docker logs woo-test-runner
docker compose down
echo "✅ Done!"
echo "📊 Opening Allure Report at http://localhost:8888"
docker run --rm -d -p 8888:80 -v "$(pwd)/allure-report:/usr/share/nginx/html" nginx
open http://localhost:8888 2>/dev/null || xdg-open http://localhost:8888 2>/dev/null || echo "Open http://localhost:8888 in your browser"