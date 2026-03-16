# 🚀 WooCommerce API Automation Testing with Python & Pytest
[![API Tests](https://github.com/christinekim8/python-api-test-automation/actions/workflows/main.yml/badge.svg)](https://github.com/christinekim8/python-api-test-automation/actions/workflows/main.yml)
[![Allure Report](https://img.shields.io/badge/Allure_Report-Live-success?logo=githubpages&logoColor=white)](https://christinekim8.github.io/python-api-test-automation/)
## 📖 Overview
This project is a high-performance API automation framework designed to validate the **WooCommerce REST API**. Built with **Python** and **Pytest**, it focuses on robust backend validation, data integrity, and end-to-end lifecycle management of e-commerce resources. 

The suite is fully containerized using **Docker** and integrated into a **CI/CD pipeline** with automated **Allure Reporting**, demonstrating a production-ready QA engineering approach.

## 🛠 Tech Stack
* **Language:** Python 3.13
* **Testing Framework:** Pytest
* **API Client:** Requests
* **Infrastructure:** Docker & Docker-Compose
* **CI/CD:** GitHub Actions
* **Reporting:** Allure Report & Pytest-HTML

## 🧪 Key Test Scenarios & Technical Highlights
Based on the [Test Scenarios Document](https://docs.google.com/spreadsheets/d/1q9Wi85kXyGIHP1X57NxOVgg75J-sA2PnZ6LEsig01g8/edit?usp=sharing), this suite covers critical business logic:

* **Full Resource Lifecycle (PRD-001 & PRD-019):**
    * Demonstrates advanced **Setup & Teardown** management using Pytest fixtures (`yield`). 
    * Ensures a clean test environment by automatically creating and permanently removing (Hard Delete) test data.
* **Data-Driven Negative Testing (PRD-003, 005, 006):**
    * Utilizes `@pytest.mark.parametrize` to validate multiple edge cases (invalid types, empty fields, malformed JSON) in a single scalable function.
* **Business Logic & State Management (PRD-007):**
    * Verifies **Duplicate SKU Validation**, ensuring the system correctly handles state transitions and data uniqueness constraints.
* **Advanced Pagination Integrity (PRD-011):**
    * Implements complex logic to verify no data overlap across multiple API pages using Python **Sets** for ID comparison.
* **Security & Authentication (PRD-017):**
    * Validates the API's security layer by asserting correct error responses (401 Unauthorized) for invalid credentials.

## 🏗 CI/CD Pipeline & Infrastructure
* **Dockerized Environment:** The entire test environment, including a local WordPress/WooCommerce instance and the Test Runner, is orchestrated via `docker-compose`.
* **GitHub Actions CI:** Every `push` or `pull_request` triggers the automated pipeline:
    1.  Spins up the Docker infrastructure.
    2.  Executes the Pytest suite.
    3.  Generates and deploys an **Allure Report** to GitHub Pages for visual stakeholder review.

## 🚀 How to Run Locally
1.  **Clone the repo:** `git clone https://github.com/christinekim8/python-api-test-automation.git`
2.  **Setup Environment:** Create a `.env` file with your `CONSUMER_KEY` and `CONSUMER_SECRET`.
3.  **Run with Docker:**
    ```bash
    docker-compose up --build
    ```
4.  **View Report:**
    ```bash
    allure serve allure-results


## 🗺 Future Roadmap
While the current version focuses on the Products category, the following expansions are planned:
Module Expansion: Implement automated test suites for Orders, Customers, and Coupons APIs.
Performance Testing: Integrate Locust to simulate high-traffic scenarios on the WooCommerce API.
