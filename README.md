# RaktaPraptih

RaktaPraptih (meaning "blood attainment" in Hindi) is a Django-based backend system designed to Blood Availability finder application. It provides secure, scalable RESTful APIs for user management, donation requests, and role-based access, built with Django REST Framework (DRF). The project leverages modern tools like Docker, GitHub Actions for CI/CD, and Render for deployment, ensuring reliability and efficiency.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Clone the Repository](#clone-the-repository)
  - [Set Up the Environment](#set-up-the-environment)
  - [Configure the Database](#configure-the-database)
  - [Run Migrations and Collect Static Files](#run-migrations-and-collect-static-files)
  - [Start the Development Server](#start-the-development-server)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Deployment](#deployment)
  - [Docker Setup](#docker-setup)
  - [CI/CD with GitHub Actions](#cicd-with-github-actions)
  - [Deploy to Render](#deploy-to-render)
- [Testing and Monitoring](#testing-and-monitoring)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
RaktaPraptih addresses the challenge of coordinating blood donation by providing a Blood Availability finder application for donors, recipients, and Blood Banks. It enables secure user registration, role-based access, and efficient management of donation requests through RESTful APIs. The system is containerized with Docker, deployed on Render, and automated with GitHub Actions for CI/CD, achieving 99.9% API availability and optimized performance.

## Features
- **User Management**: Register, login, and manage profiles with role-based access (donors, Blood Banks).
- **Donation Requests**: Request for blood donation(twillo messages).
- **Secure Authentication**: Implements JWT-based authentication for secure access.
- **Rate Limiting**: Custom throttling to ensure API stability under high traffic.
- **Scalable Deployment**: Containerized with Docker and deployed on Render with CI/CD automation.
- **Monitoring**: Integrated with Sentry for error tracking and Locust for load testing.

## Tech Stack
- **Backend**: Python, Django, Django REST Framework (DRF)
- **Database**: PostgreSQL (via Supabase)
- **Authentication**: JWT
- **DevOps**: Docker, GitHub Actions (CI/CD), Render
- **Testing & Monitoring**: pytest, Bandit, Sentry
- **Version Control**: Git, GitHub
- **Documentation**: Markdown

## Prerequisites
Before setting up the project, ensure you have the following installed:
- Python 3.11
- PostgreSQL (or a Supabase account)
- Docker and Docker Compose
- Git
- Node.js (optional, for frontend integration)
- A Render account (for deployment)
- A Supabase account (for PostgreSQL database)
- A Sentry account (for error monitoring)
- A Twillo account (for message service)

## Getting Started

### Clone the Repository
Clone the RaktaPraptih repository to your local machine:
```bash
https://github.com/Siddharthasanapala/RaktaPraptih.git
cd raktapraptih
```

### Set Up the Environment
1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   Install the required Python packages using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**:
   Create a `.env` file in the project root and add the following variables:
   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=False
   DATABASE_URL=postgres://user:password@host:port/dbname?sslmode=require
   ALLOWED_HOSTS=localhost,127.0.0.1,your-render-url
   PORT=8000
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=yourpassword
   SENTRY_DSN=your-sentry-dsn
   ```
   - Replace `DATABASE_URL` with your Supabase PostgreSQL URL.
   - Generate a `SECRET_KEY` for Django (e.g., using `django.core.management.utils.get_random_secret_key()`).
   - Set `SENTRY_DSN` if using Sentry for monitoring.

### Configure the Database
1. **Set Up Supabase**:
   - Create a free Supabase account and set up a PostgreSQL database.
   - Obtain the `DATABASE_URL` from Supabase (format: `postgres://user:password@host:port/dbname?sslmode=require`).

2. **Update Django Settings**:
   Ensure `RaktaPraptih/settings.py` uses the `DATABASE_URL` from your `.env` file for database configuration.

### Run Migrations and Collect Static Files
1. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

2. **Collect Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Create a Superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

### Start the Development Server
Run the Django development server to test the application locally:
```bash
python manage.py runserver 0.0.0.0:8000
```
Access the app at `http://localhost:8000`. The admin panel is available at `http://localhost:8000/admin`.

## API Endpoints
RaktaPraptih provides the following RESTful API endpoints (built with DRF):

| Endpoint                                 | Method | Description                     | Authentication |
|------------------------------------------|--------|---------------------------------|---------------|
| `/signup/bloodbank/`         | POST   | Register a blood bank             | None          |
| `/signup/donor/`         | POST   | Register a Donor             | None          |
| `/login/`         | POST   | Login and obtain JWT token      | None          |
| `/logout/`         | POST   | Logout       | JWT          |
| `/api/token/`         | GET    | get access and refresh tokens     | JWT           |
| `/api/token/refresh/`         | GET    | Generate new Access token with refresh token     | JWT           |
| `/api/token/verify/`         | POST    | Verify the Access token     | JWT           |
| `/bloodbank/update/<int:bloodbank_id>/`     | POST   | Update blood levels in Blood Bank       | JWT           |
| `/bloodbank/<int:pk>/`     | POST   | Get Blood Bank Details      | JWT           |
| `/donors/`     | GET    | Get List donors registered          | JWT           |
| `/donors/<int:donor_id>/`     | GET    | Get donors details          | JWT           |
| `/request/<int:donor_id>/`| POST  | Request  donor for Blood Donation     | JWT           |

### Example Request (Login)
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

## Authentication
RaktaPraptih uses **JWT (JSON Web Tokens)** for authentication:
- Register or login to obtain a JWT token.
- Include the token in the `Authorization` header for protected endpoints:
  ```
  Authorization: Bearer your-jwt-token
  ```
- Custom **throttling** is implemented to limit API requests, ensuring stability under high traffic.

## Deployment

### Docker Setup
1. **Build the Docker Image**:
   ```bash
   docker build -t raktapraptih .
   ```

2. **Run the Container Locally**:
   ```bash
   docker run -d -p 8000:8000 \
     -e SECRET_KEY=your-secret-key \
     -e DEBUG=False \
     -e DATABASE_URL=your-supabase-url \
     -e ALLOWED_HOSTS=localhost \
     raktapraptih
   ```
   Access the app at `http://localhost:8000`.

### CI/CD with GitHub Actions
The project includes a GitHub Actions workflow (`.github/workflows/ci-cd.yaml`) for automated CI/CD:
1. **Workflow Steps**:
   - Run unit tests with pytest.
   - Perform security scans with Bandit.
   - Build and push Docker image to Docker Hub.
   - Deploy to Render via a deploy hook.
2. **Configure Secrets**:
   Add the following secrets to your GitHub repository:
   - `DOCKER_USERNAME`: Your Docker Hub username.
   - `DOCKER_PASSWORD`: Your Docker Hub password.
   - `RENDER_DEPLOY_HOOK_URL`: Your Render deploy hook URL.
3. **Trigger CI/CD**:
   Push changes to the `main` branch to trigger the workflow.

### Deploy to Render
1. **Set Up Render**:
   - Create a free Render account and set up a new web service.
   - Select "Docker" as the environment and link your Docker Hub repository (`your-username/raktapraptih`).
2. **Configure Environment Variables**:
   Add the same `.env` variables as above in Render’s environment settings.
3. **Deploy**:
   Trigger deployment manually or via GitHub Actions. The app will be live at `your-app-name.onrender.com`.

## Testing and Monitoring
- **Unit Tests**: Run tests with pytest:
  ```bash
  pytest
  ```
- **Load Testing**: Use Locust to simulate traffic:
  ```bash
  locust -f locustfile.py --host=http://localhost:8000
  ```
- **Security Scanning**: Scan for vulnerabilities with Bandit:
  ```bash
  bandit -r .
  ```
- **Error Monitoring**: Configure Sentry using the `SENTRY_DSN` in your `.env` file to track runtime errors.

## Directory Structure
```
RaktaPraptih/
├── RaktaPraptih/         # Django project settings and WSGI
│   ├── __init__.py
│   ├── settings.py
│   ├── asgi.py
│   ├── throttles.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                 # DRF app for API endpoints
│   ├── migrations/
│   ├── models.py
│   ├── forms.py
│   ├── permissions.py
│   ├── context_processers.py
│   ├── utils.py
│   ├── tests.py
│   ├── utils.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── donors/                 
│   ├── migrations/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
├── scripts/             # Startup and utility scripts
│   └── start.sh
├── .github/             # CI/CD workflows
│   └── workflows/
│       └── ci-cd.yaml
├── static/             
│   ├── JS
│   └── css
├── Templates/             
│   ├── landingpage.html
│   ├── --
│   ├── --
│   └── --
├── Dockerfile           # Docker configuration
├── docker-compose.yaml           
├── render.yaml           
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
