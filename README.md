# Multiset-backend

## Current Features
1. Google authentication
2. Group management
3. Purchase splitting
4. Purchase settlements
5. Analytics
6. Group grocery list

Note: To try out the API endpoints after starting the application, go to `/api/docs` where you can use the interactive frontend.

## Setup

To setup the backend, you can either do it locally or using the docker container. Note that the database is cloud-hosted via AWS RDS so you do not have to load the sample data into your local database.

### Docker Setup

1. Start docker desktop
2. Create a `.env` file at the root with the secrets (message Emma)
3. Run the following command:

```bash
docker-compose up -d
```

### Local Setup

1. Create a python environment and activate:

```bash
python -m venv env

source env/bin/activate
```

2. Install the dependencies

```bash
pip3 install -r requirements.txt
```

3. Run the server

```bash
./manage.py runserver
```
