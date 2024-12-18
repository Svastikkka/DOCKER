# Docker Environment Setup

## Introduction
This repository contains the necessary files and instructions to set up a local environment using Docker and Docker Compose. The setup includes a wide range of services for various use cases, such as workflow management, data integration, monitoring, and secure secret storage. The Docker Compose YAML file provided in this repository deploys the following services:

- **Airflow**: An open-source workflow management platform.
- **Minio**: An object storage server.
- **MySQL**: A relational database management system (RDBMS).
- **Selenium (Python)**: A browser automation tool, ideal for functional testing.
- **Vault**: A secure secrets storage solution.
- **Kafka**: A distributed streaming platform.
- **MongoDB**: A document-oriented NoSQL database.
- **ZooKeeper**: A centralized service for maintaining configuration information.
- **Jenkins**: An open-source automation server.
- **Keycloak**: An identity and access management solution.
- **KrakenD**: An ultra-fast API gateway.
- **Nexus**: A repository manager for storing and managing software components.
- **NiFi**: A data integration and processing framework.
- **Wiki.js**: A modern and powerful wiki platform.
- **Grafana Stack**: A comprehensive monitoring and visualization solution.
- **PostgreSQL Replication**: Enables database replication across PostgreSQL instances.
- **PostgreSQL Logical Replication**: Supports advanced replication using pglogical.


## Prerequisites
Before setting up the local environment, ensure you have the following installed on your system:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Setup Instructions
Follow these steps to set up the local environment:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Svastikkka/DOCKER.git
   ```

2. **Navigate to the Repository Directory**:
   ```bash
   cd <repository-directory>
   ```

3. **Update Configuration**:
   Modify the `docker-compose.yml` file according to your requirements. This may include changing port numbers, environment variables, or volume mounts.

4. **Start the Docker Containers**:
   ```bash
   docker-compose up -d
   ```
   This command will build and launch the containers in detached mode. To view logs in the console, omit the `-d` flag.

5. **Verify the Container Status**:
   ```bash
   docker-compose ps
   ```
   Ensure all containers are running properly.

## Additional Notes

- Each service may require specific configuration. Refer to the respective service's documentation for further details.
- Ensure your system has sufficient resources (CPU, memory, etc.) to run all containers smoothly.

### Stopping the Environment
To stop and remove all containers, use:
```bash
docker-compose down
```

## Troubleshooting
If you encounter issues:

- Verify that Docker and Docker Compose are up-to-date.
- Ensure required ports in `docker-compose.yml` are not in use.
- Check container logs for errors using:
  ```bash
  docker logs <container_name>
  ```

For further assistance, consult the respective service documentation or raise an issue in this repository.