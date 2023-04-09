# Stage 1: Base image
FROM python:3.10-slim-buster AS base
WORKDIR /app

# Install PostgreSQL and RabbitMQ
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    postgresql-client \
    postgresql \
    rabbitmq-server && \
    rm -rf /var/lib/apt/lists/*

# Stage 2: Python setup
FROM base AS python
WORKDIR /app
# Set the environment variable for the Python application
ENV DATABASE_URL=postgresql://postgres:mysecretpassword@localhost:5432/kts_project
# Install required Python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application code to the container
COPY . .

# Stage 3: PostgreSQL setup
#FROM base AS postgres
# Start PostgreSQL and set password for 'postgres' user
RUN service postgresql start && \
    su - postgres -c "psql --command \"ALTER USER postgres WITH PASSWORD 'mysecretpassword';\"" && \
    service postgresql stop
# Create a new PostgreSQL database 'kts_project' and grant all privileges to the 'postgres' user
RUN service postgresql start && \
    su - postgres -c "createdb kts_project -O postgres" && \
    su - postgres -c "psql --command \"GRANT ALL PRIVILEGES ON DATABASE kts_project TO postgres;\"" && \
    service postgresql stop

# Stage 4: Fill the database with data
#FROM postgres AS fill_db
# Copy the SQL scripts to the container
COPY etc/sql/create_database.sql /app/create_database.sql
COPY etc/sql/fill_database.sql /app/fill_database.sql
# Log the existing databases in PostgreSQL
RUN service postgresql start && \
    su - postgres -c "PGPASSWORD=mysecretpassword psql -h localhost -U postgres -h localhost -c \"\l\"" && \
    # Run the SQL script to create database and tables
#    su - postgres -c "psql -c 'CREATE DATABASE kts_project'" && \
    su - postgres -c "PGPASSWORD=mysecretpassword psql -h localhost -U postgres -d kts_project -a -f /app/create_database.sql" && \
    # Run the SQL script to fill tables with data
    su - postgres -c "PGPASSWORD=mysecretpassword psql -h localhost -U postgres -d kts_project -a -f /app/fill_database.sql" && \
    service postgresql stop


# Stage 5: RabbitMQ setup
FROM base AS rabbitmq
# Start the RabbitMQ server
RUN service rabbitmq-server start && \
    rabbitmqctl add_user myuser mypassword && \
    rabbitmqctl add_vhost myvhost && \
    rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*" && \
    service rabbitmq-server stop

# Stage 6: Final image
FROM python AS final
# Copy PostgreSQL and RabbitMQ setup from previous stages
#COPY --from=postgres /app /app
COPY --from=rabbitmq /etc/rabbitmq /etc/rabbitmq

EXPOSE 8080
# Check PostgreSQL connection before starting RabbitMQ and Python application
CMD service postgresql start && \
    service rabbitmq-server start && \
    python main.py
