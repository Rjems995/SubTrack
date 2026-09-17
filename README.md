SubTrack - Subscription Manager

SubTrack ("Track Your Subscriptions") is a clean, modern, and responsive web application designed to help you organize, monitor, and optimize your monthly and annual recurring expenses.

Features

Mobile-First & Fully Responsive: Optimized for smartphones, tablets, and desktop devices with touch-friendly navigation, mobile drawers, and floating action buttons (FAB).

Interactive Analytics & Spending Insights: Visual breakdown of your expenses powered by Chart.js, featuring:

Multi-color Category Breakdown Doughnut Chart.

Monthly Schedule Projection Bar Chart.

Multi-Color Category Tagging: Instant visual distinction across Entertainment, Productivity, Utilities, Health & Fitness, SaaS, Education, Shopping, and Custom categories.

Renewal Alerts & Urgency Notifications: Banner reminders for active subscriptions renewing within 3 days.

Dark / Light Mode: Seamless theme toggling tailored for daytime viewing or dark interface preferences.

Data Privacy & Storage: Works out-of-the-box locally in your browser using localStorage.

Import & Export: Backup and restore your subscription data at any time via JSON files.

Python FastAPI + SQLite Backend: Optional lightweight REST API backend to sync and persist your data to a SQLite database.

Project Structure

subtrack/
├── index.html               # Single-file Frontend App (HTML5 + Tailwind CSS + JS)
├── main.py                  # Python REST API Backend (FastAPI + SQLite)
├── github_upload_guide.md   # Deployment Guide for GitHub Pages
└── README.md                # Project Documentation


Quick Start

Option 1: Running the Frontend (No Backend Required)

Since index.html is fully self-contained, you can run the application directly in any modern web browser:

Double-click index.html or drag and drop it into your favorite browser.

Start adding and tracking your subscriptions right away! Data will be saved locally in your browser.

Option 2: Running with the Python Backend (FastAPI + SQLite)

To use SubTrack with a persistent SQLite database service on your machine:

Prerequisites

Python 3.8 or higher installed on your computer.

Steps

Install required dependencies:

pip install fastapi uvicorn pydantic


Start the FastAPI server:

uvicorn main:app --reload


Access the API:

The server will start at http://127.0.0.1:8000.

View interactive Swagger API documentation at http://127.0.0.1:8000/docs.

Deploying to GitHub Pages (Free Hosting)

You can host SubTrack live on the web for free using GitHub Pages:

Create a new public repository on GitHub.

Upload index.html to the repository.

Go to Settings > Pages.

Set the source branch to main (or master) and save.

GitHub will generate your live URL (e.g., https://yourusername.github.io/repository-name/).

(For detailed step-by-step instructions, see github_upload_guide.md).

Built With

Frontend: HTML5, Tailwind CSS, Vanilla JavaScript (ES6+)

Charts & Graphics: Chart.js, Lucide Icons

Backend (Optional): Python 3, FastAPI, SQLite3, Uvicorn

License

This project is open source and available under the MIT License.
