# SIMANTAP Backend
## Description
This is the backend service for the SIMANTAP SIstem Manajemen ANTrian Administrasi dan bimbingan Prodi. An application to help managing [Antrian Administrasi dan Bimbingan Program Studi Teknik Informatika ITERA]. This application using Python FastAPI to serve backend and React to serve frontend side <a href="https://github.com/muhammadfabil/tea">Frontend Repo</a> or you can test the fully running application <a href:"https://simantap.ifsyscenter.my.id">Here</a>. 

## Features
- [Feature 1]: YADA YADA YADA
- [Feature 2]: JUST CHECK THE APP
- [Feature 3]: FastAPI, JWT, Websocket, Web Push
- Just contact me or whatever if you got problems or questions

## Getting Started

Follow these steps to set up the project after cloning the repository:

### Prerequisites
Ensure you have the following installed:
- Python (i don't know minimun but i use version 3.12.6)
- pip (i'm using version 25.0.1)
- Postgresql or any SQLdatabase
- Supabase or anything for storage
- Sanity, and Sheer Willpower

### Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/BangKumish/backend.git
    cd Project_TA/backend
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activated
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Database Migrations with Alembic**:
    - Initialize Alembic:
        ```bash
        alembic init migrations
        ```
    - Configure the `alembic.ini` file and the `env.py` file in the `migrations` directory as needed.
    - Generate a new migration script:
        ```bash
        alembic revision --autogenerate -m "Initial migration"
        ```
    - Apply the migration to the database:
        ```bash
        alembic upgrade head
        ```

5. **Setup your own environment**:
    - Create your own .env and supply it with your database url mine using postgres
    - Should've at least looked like this
        ```bash
            cors_origins = ["*"]
            frontend_url = "https://simantap.ifsyscenter.my.id" # update using your frontend

            DATABASE_URL="postgresql://username:password@localhost:port/database_name"

            SECRET_KEY="secret key for your JWT, use online generator"

            VAPID_PRIVATE_KEY="vapid key for your push notification"
            VAPID_PUBLIC_KEY="use python vapid generator to generate"
            INCLUDE_HEADER = "or use online vapid key generator"
            APPLICATION_SERVER_KEY = "it really doesnt care where you got your key"

            ALGORITHM="HS256"
            ACCESS_TOKEN_EXPIRE_MINUTES="15" # 1,2,10,60 put whatever you like

            SUPABASE_URL="your OWN supabase url dont use ours" 
            SUPABASE_KEY="THIS IS MY KEY. THERE'R MANY LIKE IT, BUT THIS ONE IS MINE."
            SUPABASE_BUCKET = "make your own supabase and make your own bucket name"

            SMTP_HOST="smtp.gmail.com or any privider you like there'r plenty of 'em"
            SMTP_PORT=587
            SMTP_USER="this one is ours don't use please"
            SMTP_PASSWORD="Well you cant use our email unless you know this part""
        ```

6. **Run the Application**:
    ```bash
    uvicorn app.main:app --reload
    ```

Hey dont forget to give us a star, 1 star equal to 100 love for devs