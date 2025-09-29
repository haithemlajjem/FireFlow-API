# FireFlow API

FireFlow is a RESTful API for managing firewalls, policies, and rules. It provides endpoints to create, update, delete, and retrieve firewalls, policies, and rules, ensuring proper validation and database integrity.

---

## Business Logic

### Firewalls
- **Create Firewall**: A firewall is created with a unique name and an optional description. Duplicate names are not allowed.
- **Update Firewall**: Allows updating the name and description of an existing firewall. The name must remain unique.
- **List Firewalls**: Retrieves all firewalls in the system.
- **Get Firewall**: Fetches a specific firewall by its ID.
- **Delete Firewall**: Deletes a firewall by its ID. Associated policies and rules are also deleted due to cascading.

### Policies
- **Add Policy**: A policy is associated with a specific firewall. It contains a list of rules.
- **List Policies**: Retrieves all policies for a given firewall.
- **Delete Policy**: Deletes a policy and its associated rules.

### Rules
- **Add Rule**: A rule is added to a policy with attributes like action (`allow` or `deny`), source, destination, and protocol.
- **List Rules**: Retrieves all rules for a given policy.
- **Delete Rule**: Deletes a specific rule by its ID.

---

## How to Run the Project

### Prerequisites
- Python 3.9 or higher
- Docker (optional)
- Poetry (for dependency management)

---

### Run Without Docker

1. **Clone the Repository**
   ```bash
   git clone https://github.com/haithemlajjem/FireFlow-API.git
   cd FireFlow-API
2. **Set Up Virtual Environment**
    ```bash
   poetry install
3. **Set Environment Variables Create a .env file in the root directory**
    ```bash
    FLASK_ENV=development
    SQLALCHEMY_DATABASE_URI=sqlite:///fireflow.db
4. **Run the Application**
    ```bash
    poetry run flask run
5. **Access the API**
    * Base URL: http://localhost:5000
    * Swagger Docs: http://localhost:5000/apidocs

### Run With Docker

1. **Build the Docker Image**
   ```bash
   docker build -t fireflow-api .
2. **Run the Docker Container**
    ```bash
    docker run -p 5000:5000 --env-file .env fireflow-api


# Improvements to Add

1. **Authentication and Authorization**
   - Add user authentication (e.g., JWT tokens) to secure the API.
   - Implement role-based access control (RBAC) for different user roles.

2. **Pagination**
   - Implement pagination for listing endpoints (e.g., firewalls, policies, rules).

3. **Error Handling**
   - Add custom error handlers for better error messages and HTTP status codes.

4. **Testing**
   - Expand unit tests to cover edge cases and invalid inputs.
   - Add **integration tests** to verify interactions between services, database, and API endpoints.
   - Implement **end-to-end (E2E) tests** for full API workflows (firewall → policy → rule).

5. **Database Migrations**
   - Use Alembic for managing database migrations.
   - Version control schema changes and allow safe upgrades.

6. **Rate Limiting**
   - Add rate limiting to prevent abuse of the API.

