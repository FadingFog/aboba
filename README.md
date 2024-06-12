# Alar Studios® Test Task

## Quick start
### Prerequisites
* Python 3.12.2
### Installing

1. Create a personal fork of this repository.

2. **Clone** the fork with HTTPS/SSH, using your local terminal to a preferred location, and **cd** into the project.
3. Create virtual environment, and install dependencies.
    ```bash
    > poetry install
    ```
4. Create an .env file or put the parameters directly in the environment variables from `.env.sample`.
5. Deploy docker compose.
    ```bash
    > docker compose up
    ```
6. Populate your database tables according to model and send request to `http://127.0.0.1:8000/` to get result.