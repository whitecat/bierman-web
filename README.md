# Beirman Web Project

This repository contains a Django backend and a React frontend (using Vite) for the Beirman web application. Note: The analysis features only support projects containing .kt, .py, or .java files. The backend handles property data and analysis, while the frontend provides a modern user interface.

## Prerequisites

- Python 3.11+ (for the backend)
- Poetry (for Python dependency management)
- Node.js 22.12.0+ (for the frontend)
- Yarn (package manager for frontend dependencies)

## Project Structure

```
beirman-web/
│── backend/               # Django backend
│   ├── backend/           # Django project settings
│   ├── analyze/           # Django app for handling property data and analysis
│   │   ├── analysis/      # Code analysis logic
│   │   ├── core/          # Codebase utilities
│   │   ├── questions/     # Question generation logic
│   │   ├── summarization/ # Summarization logic
│   │   ├── utils/         # Utility functions
│   │   ├── tests/         # Unit tests for backend modules
│   ├── manage.py          # Django management script
│   ├── poetry.lock        # Poetry dependency lock file
│   ├── pyproject.toml     # Python dependencies and settings
│   ├── .env               # Environment variables for Django
│── frontend/              # React frontend with Vite
│   ├── src/               # React source code
│   │   ├── services/      # API service logic
│   │   ├── types/         # TypeScript types
│   │   ├── tests/         # Frontend test setup
│   ├── public/            # Static assets
│   ├── package.json       # Frontend dependencies
│   ├── vite.config.ts     # Vite configuration
│   ├── .env               # Environment variables for React
│── assets/                # Project images and assets
│── README.md              # Project documentation
│── LICENSE                # Licensing information
```

### Backend (Django) Setup

The backend is a Django application using Poetry for dependency management.

**Step 1:** Install Dependencies
Navigate to the backend folder and install dependencies:

```bash
cd backend
poetry install
```

**Step 2:** Set Up Environment Variables
Copy the sample `.env` file and configure your environment variables:

```bash
cp .env.example .env
```

Modify `.env` as needed:

```bash
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
OPENAI_API_KEY=your_openai_api_key
```

**Step 3:** Install and Start a Poetry Shell
To install the Poetry Shell, run:

```bash
poetry self add poetry-plugin-shell
```

To activate the virtual environment, run:

```bash
poetry shell
```

**Step 4:** Run the Backend
Once inside the Poetry shell, start the Django server:

```bash
python manage.py runserver
```
The backend will now be running at [http://localhost:8000](http://localhost:8000).

### Frontend (React + Vite) Setup

The frontend is a React app powered by Vite.

**Step 1:** Install Dependencies

Navigate to the frontend folder and install dependencies:

```bash
cd frontend
yarn install
```

**Step 2:** Set Up Environment Variables

Copy the sample `.env` file and configure your environment variables:

```bash
cp .env.example .env
```

Modify `.env` as needed:

```bash
VITE_BACKEND_API_URL=http://localhost:8000
```

**Step 3:** Run the Frontend

Start the frontend development server:

```bash
yarn dev
```

The frontend will be available at [http://localhost:5173](http://localhost:5173).

## Running Tests

The following sections provides instructions for running the test suites associated with the frontend and backend.

### Backend (Django)

To run Django tests, first enter the Poetry shell:

```bash
cd backend
poetry shell
```

Then, run:

```bash
python manage.py test
```

### Frontend (React + Vitest)

To run frontend tests:

```bash
cd frontend
yarn test
```

## API Endpoints

The backend currently exposes a single API endpoint.

| Method | Endpoint       | Description             |
|--------|----------------|-------------------------|
| Post   | /analyze/url/  | Analyze project by URL  |
| Post   | /analyze/file/ | Analyze project by file |

## Troubleshooting

- Backend Issues
  - Ensure `poetry` is installed correctly (`pip install poetry`).
  - Check `.env` for missing variables.

- Frontend Issues
  - Delete `node_modules` and reinstall dependencies:

    ```bash
    rm -rf node_modules yarn.lock
    yarn install
    ```
