# Fit Roulette

FitRoulette is an interactive web application designed to make fitness training sessions more engaging and fun for school-aged children (7-17 years old), including those with disabilities. 
It introduces elements of control, surprise, and special effects to keep the kids motivated and interested in their exercises. The game is played online with a teacher leading the sessions.

## Requirements

To run this project, you need:

- Python (version 3.11)
- Django (version 5.0.4)
- asgiref (version 3.8.1)
- sqlparse (version 0.5.0)
- tzdata (version 2024.1)

## Installation and Setup

1. Clone this repository:

    ```bash
    git clone https://github.com/michailivanov/FitRoulette.git
    ```

2. Navigate to the project directory:

    ```bash
    cd FitRoulette
    ```

3. Set up a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate      # On macOS/Linux
    .\venv\Scripts\activate      # On Windows
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

## Run Server

To start the development server, run:

  ```bash
  python manage.py runserver
  ```
