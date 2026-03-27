# 🚀 WooCommerce API Automation Testing with Python & Pytest
[![Build Status](https://img.shields.io/github/actions/workflow/status/christinekim8/python-api-test-automation/main.yml?style=for-the-badge&logo=github-actions&label=Build)](https://github.com/christinekim8/python-api-test-automation/actions)
[![Allure Report](https://img.shields.io/badge/Allure%20Report-Live%20Dashboard-yellowgreen?style=for-the-badge&logo=allure)](https://christinekim8.github.io/python-api-test-automation/)

## 📖 Overview
This project is a high-performance API automation framework designed to validate the **WooCommerce REST API**. Built with **Python** and **Pytest**, it focuses on robust backend validation, data integrity, and end-to-end lifecycle management of e-commerce resources.

The suite is fully containerized using **Docker** and integrated into a **CI/CD pipeline** with automated **Allure Reporting**, demonstrating a production-ready QA engineering approach.

## 💡 Background & Design Decision
This project was initially deployed on **AWS EC2** with a full Docker environment. However, running a dedicated EC2 instance 24/7 solely for portfolio purposes introduced unnecessary infrastructure costs.

The architecture was redesigned to be **fully self-contained**: the entire test environment (WordPress, WooCommerce, MySQL) spins up on-demand via Docker Compose — locally or in GitHub Actions — and tears down automatically after tests complete. This approach ensures:
- ✅ **Zero hosting costs** — no persistent server required
- ✅ **Runs anywhere** — any machine with Docker Desktop installed
- ✅ **Fully automated** — triggered on every `git push` via GitHub Actions

## 🛠 Tech Stack
| Category | Technology |
|----------|-----------|
| Language | Python 3.13 |
| Testing Framework | Pytest |
| API Client | Requests |
| Infrastructure | Docker & Docker Compose |
| CI/CD | GitHub Actions |
| Reporting | Allure Report |
| System Under Test | WordPress + WooCommerce (Docker) |
| Database | MySQL 8.0 (Docker) |

## 🏗 Architecture
```
git push
    └── GitHub Actions
            ├── docker compose up
            │       ├── woo-db (MySQL)
            │       ├── woo-app (WordPress + WooCommerce)
            │       ├── wp-setup (WP-CLI auto-install)
            │       └── woo-test-runner (pytest + Allure)
            ├── Allure Report generated
            └── Deploy to GitHub Pages
```

## 🧪 Key Test Scenarios & Technical Highlights
> 📋 Full test scenarios documented in **[Test Scenarios Spreadsheet](https://docs.google.com/spreadsheets/d/1q9Wi85kXyGIHP1X57NxOVgg75J-sA2PnZ6LEsig01g8/edit?gid=0#gid=0)** — currently covers the **Products** category.

| Test Case | ID | Description |
|-----------|-----|-------------|
| Full Resource Lifecycle | PRD-001, PRD-019 | Create → Verify → Hard Delete using `yield` fixtures |
| Negative Testing | PRD-003, PRD-005 | `@pytest.mark.parametrize` for invalid inputs |
| Duplicate SKU Validation | PRD-007 | Business logic & state management |
| Pagination Integrity | PRD-011 | No data overlap across pages using Python Sets |

## 🚀 How to Run Locally

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed

### Run Tests

**Windows:**
```bat
run.bat
```

**Mac/Linux:**
```bash
chmod +x run.sh
./run.sh
```

That's it! The script will:
1. Spin up WordPress + WooCommerce + MySQL in Docker
2. Auto-install WooCommerce and configure API credentials
3. Run all pytest test cases
4. Generate Allure report
5. Serve the report at **http://localhost:8888** — opens automatically in your browser

### View Latest Report
View the latest CI report on **[GitHub Pages](https://christinekim8.github.io/python-api-test-automation/)**.

## 🗺 Future Roadmap
- **Module Expansion:** Implement automated test suites for Orders, Customers, and Coupons APIs
- **Performance Testing:** Integrate Locust to simulate high-traffic scenarios
- **Contract Testing:** Add Pact for consumer-driven contract testing