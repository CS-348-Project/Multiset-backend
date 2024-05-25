# CS-348-Project

## Setup
To setup the backend, you can either do it locally or using the docker container.

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
