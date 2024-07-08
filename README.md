# Multiset-backend

## Current Features

1. Google authentication
2. Group management
3. Purchase splitting
4. Purchase settlements
5. Analytics
6. Group grocery list
7. Debts and optimization

## API Docs

To try out the API endpoints after starting the application, go to `/api/docs` where you can use the interactive frontend. In order to access endpoints protected by auth, you would need to set the bearer token through the Authorize button at the top right of the page. Please message Emma for a valid token value that you can use!

To see our test SQL queries, go into the `tests` folder from the root directory of the repository. In this folder, there is a subfolder called `suites` that has the test SQL queries and a folder called `outputs` which has the corresponding results of the tests.

## Setup

Since our GitHub includes the prod dataset with high volumes of data that exceed Git limitations, you will need to install [git-lfs](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage) before cloning the database locally. Below are the two commands you would need to run in order to install git-lfs:

```bash
brew install git-lfs
git lfs install
```

To setup the backend, you can run a docker container through the Makefile. This approach eliminates possible issues with environment inconsistencies.

1. Start docker desktop
2. Create a `.env` file at the root with the secrets (message Emma)
3. Run the following command:

```bash
make init
```

To stop running all services, run the following command:

```bash
make down
```

## Useful Make Commands

Below are useful Makefile commands to manage the Docker containers for our Django application.

### Build Docker Images

```bash
make build
```

Builds all necessary Docker images from the Dockerfile, preparing the environment.

### Start Services

```bash
make up
```

Launches all services defined in docker-compose.yml in detached mode.

### Apply Django Migrations

```bash
make migrate
```

Executes Django migrations to update or set up the database schema.

### Seed Database

```bash
make seed
```

Runs a custom Django management command to populate the database with initial data.

### Stop All Services

```bash
make down
```

Stops and removes all Docker containers, clearing the environment.

### Full Environment Initialization

```bash
make init
```

Performs a complete setup (build, start, migrate, seed), useful for first-time setups or reinitializations.

### Reinitialize Environment

```bash
make reinit
```

Fully resets and restarts the environment, useful for significant changes or clean starts.
