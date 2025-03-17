# Task Management System 🚀

Welcome to the **Task Management System** — an advanced, high-performance system designed to streamline task tracking and management. This system allows users to create tasks, assign them to others, and track their progress efficiently, even when working with large data sets.

### 📋 Project Overview

The **Task Management System** enables efficient management of tasks, user assignments, and notifications in real-time. Built with **Django** and **Django REST Framework (DRF)**, it incorporates features such as **JWT-based authentication**, **background task processing using Celery & Redis**, **WebSocket real-time updates**, and **multi-threaded report generation** for large datasets.

With **multi-threading** support and the ability to process over 100,000 tasks asynchronously, this system is designed for high performance and scalability.

---

### 🛠 Features

- **User Registration & Authentication**
  - JWT-based authentication using **Django REST Framework**.
  - Users can register, log in, and manage their profiles securely.

- **Task Management**
  - Users can create, view, update, and delete tasks with details such as:
    - Title
    - Description
    - Priority
    - Due Date
    - Status
    - assigned_to
  - Tasks can be assigned to users.
  - **Pagination & Filtering**: Filter tasks by priority, status, or due date for easy management.

- **Multi-Threaded Report Generation**
  - Generate detailed reports for large datasets (over 100,000 tasks).
  - Insights include:
    - total no of tasks
    - total completed tasks
    - total pending tasks
    - tasks order by the priority [Low, Medium, High, Urgent]
    - tasks order by the status [ Pending, In Progress, Completed, Archieved ]
    - tasks order by the user assigned to [ username ]
    - tasks order by the user created [ username ]
    - tasks order by the due date [status = pending for and due in 24 hr ]

- **Asynchronous Notifications**
  - Use **Celery** for background tasks to send notifications via email when:
    - task is created and assigned to user
    - task is updated for the required user
    - when the due date is there befor 24 hrs at 10 AM
 
  - **Redis** is used as the message broker for **Celery**.

- **Caching for Fast Data Retrieval**
  - Task list API responses are cached using **Redis** to reduce database load and improve performance for frequently accessed data.

- **Real-Time Updates with WebSockets**
  - Integrated with **Django Channels**, the system sends real-time updates via **WebSockets** when a task is updated or assigned.

---

### 🧑‍💻 Tech Stack

- **Django** & **Django REST Framework (DRF)**: For robust backend API development.
- **JWT (JSON Web Tokens)**: Secure user authentication and authorization.
- **PostgreSQL**: The relational database to store user and task data.
- **Celery** & **Redis**: For asynchronous task handling and background processing.
- **Django Channels** & **WebSockets**: For real-time task updates and notifications.
- **Docker**: Containerization for easy deployment and scalability.
- **uvicorn[standard]**: For Asynchronous operations for websockets

---

### ⚙️ How It Works

1. **User Registration & Authentication**:
   - Users register via the API, and authentication is done using **JWT tokens**.
   
2. **Task Management**:
   - Users can create, view, update, or delete tasks.
   - Tasks are assigned to users, and users can filter tasks by priority, status, or due date.

3. **Background Processing & Notifications**:
   - When a task is created or updated, **Celery** sends out notifications, like email alerts, to the users.
   - **Redis** serves as the Celery broker for managing asynchronous tasks.

4. **Report Generation**:
   - A report generation API processes large datasets asynchronously to produce task insights.
   - Multi-threading improves the processing time for large task datasets.

5. **Real-Time Task Updates**:
   - Using **Django Channels** and **WebSockets**, the system provides real-time updates whenever a task is assigned, updated, or deleted.

---

### ⚡ Performance and Scalability

- **High-Performance Architecture**: By incorporating **multi-threading** for report generation and caching with **Redis**, the system can handle a large number of tasks without performance degradation.
- **Fault Tolerance**: The use of **Celery** provides retry mechanisms and exception handling, ensuring that background tasks are processed reliably.
- **Scalable**: The architecture is built to scale, enabling you to add new features, tasks, or integrations in the future easily.

---

### 🚀 Getting Started

To get started with the **Task Management System**, follow the steps below to set up your local development environment:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/task-management-system.git
   cd task-management-system

2. **Set Up Environment Variables**:

   After cloning the repository, the next step is to configure the environment variables. These variables will be automatically loaded by Docker when you run the project.

   - In the root directory of your project (where the `docker-compose.yml` file is located), create a `.env` file to store your environment variables.

```bash
          task-management-system/
          ├── docker-compose.yml      # Docker Compose configuration file
          ├── .env                   # Environment variables file (create this)
          ├── manage.py              # Django project management script
          ├── taskManagement/       # Django app directory
          ├── requirements.txt       # Python dependencies
          ├── Dockerfile             # Dockerfile for the web service
          └── README.md              # Project documentation
```

   - Add the following configuration to the `.env` file:

   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_ID=email@gmail.com
   EMAIL_PASSWORD=email_app_password
```

3. **Build and Start the Docker Containers**:

   Now that your environment variables are set up, the next step is to build and start the Docker containers. This will ensure that your application and database are correctly configured and running.

   - In the root directory of the project (where your `docker-compose.yml` file is), run the following command to build the Docker containers:

   ```bash
   docker-compose up --build -d


4. **Run Database Migrations**:

   After building and starting the Docker containers, the next step is to apply the database migrations to set up the database schema. Follow the steps below to get into the backend container and run the migrations:

   - To enter the backend container (the `django_app` container), run the following command:

   ```bash
   docker-compose exec web bash
   ```
   OR
   ```bash
   docker-compose exec web sh

5. **Apply Database Migrations**:
   
    Once you have entered the backend container, the next step is to apply the migrations to set up the database schema.

   - Inside the container, run the following Django management command to apply the migrations:

   ```bash
   python manage.py migrate

6. **Create a Superuser**:

   After applying the migrations, you’ll need to create a superuser to access the Django admin panel and manage the application.

   - To create a superuser, run the following command inside the backend container:

   ```bash
   python manage.py createsuperuser


## 📡 API Endpoints and Response

The **Task Management System** exposes a set of RESTful APIs for managing tasks, users, and notifications. Below is an overview of the key API endpoints, including their descriptions, request methods, and expected responses.


### Authentication

#### 1. **POST** `http://localhost:8000/api/users/`  
  Registers a new user. 
  **Request Body**:
  ```json
  {
    "username": "user123",
    "email": "user123@example.com",
    "password": "password123",
    "first_name": "user1",
    "last_name": "last_name"
  }


  ```
**Response**:
  ```json
      {
        "id":1,
        "username": "user123",
        "email": "user123@example.com",
        "first_name": "user1",
        "last_name": "last_name"
       
      }

```

#### 2. **POST** `http://localhost:8000/api/token/`  
  Login user. 
  **Request Body**:
  ```json
      {
        "username": "user123",
        "password": "password123",
        
      }
  ```
  **Response**:
  ```json
            {
            "refresh": "refresh_token",
            "access": "access token",
            }  
  ```


#### 1. **GET & PUT & PATCH & DELETE ** `http://localhost:8000/api/users/{id}`  
  update specific user. 
  **Request Body**:
```json
  {
    "username": "user123",
    "email": "user123@example.com",
    "password": "password123",
    "first_name": "user1",
    "last_name": "last_name"
  }


```
**Response**:
  ```json
      {
        "id":1,
        "username": "user123",
        "email": "user123@example.com",
        "first_name": "user1",
        "last_name": "last_name"
       
      }

```


### Task Mangement
#### 1. **POST** `http://localhost:8000/api/task/`  
  Add a new task. 
  **Request Body**:
  ```json 
            {
              "title": "Task Title Example",
              "description": "This is a detailed description of the task.",
              "priority": "HIGH",
              "status": "IN_PROGRESS",
              "due_date": "2025-03-31",
              "assigned_to": 2  // ID of the user assigned to the task
            }
  ```

**Response**:
```json
            {
              "id": 1,
              "title": "Task Title Example",
              "description": "This is a detailed description of the task.",
              "priority": "HIGH",
              "status": "IN_PROGRESS",
              "due_date": "2025-03-31",
              "assigned_to": 2  // ID of the user assigned to the task
            }
```


#### 2. **GET** `http://localhost:8000/api/task?`  

#### Description:
This endpoint retrieves a list of tasks with optional filters. You can filter the tasks based on priority, status, and due date ranges.

#### Request Parameters:
You can use the following query parameters to filter the tasks:

- **priority**: Filter tasks by priority.
    - Possible values: `LOW`, `MEDIUM`, `HIGH`, `URGENT`
  
- **status**: Filter tasks by status.
    - Possible values: `PENDING`, `IN_PROGRESS`, `COMPLETED`, `ARCHIVED`
  
- **due_date**: Filter tasks by a specific due date.
    - Format: `YYYY-MM-DD`
  
- **due_date_gte**: Filter tasks with a due date greater than or equal to the specified date.
    - Format: `YYYY-MM-DD`
  
- **due_date_gt**: Filter tasks with a due date strictly greater than the specified date.
    - Format: `YYYY-MM-DD`
  
- **due_date_lte**: Filter tasks with a due date less than or equal to the specified date.
    - Format: `YYYY-MM-DD`
  
- **due_date_lt**: Filter tasks with a due date strictly less than the specified date.
    - Format: `YYYY-MM-DD`

#### Example Request:
```bash
GET /api/task?priority=HIGH&status=IN_PROGRESS&due_date_gte=2025-03-01&due_date_lte=2025-03-31
```

**Response**:
```json
            {
              "id": 1,
              "title": "Task Title Example",
              "description": "This is a detailed description of the task.",
              "priority": "HIGH",
              "status": "IN_PROGRESS",
              "due_date": "2025-03-31",
              "assigned_to": 2  // ID of the user assigned to the task
            }
```

### 3. API Endpoint: **GET & PUT & PATCH & DELETE** `/api/task/{id}`

#### Description:
This endpoint retrieves the details of a specific task by its `id`.

#### Example Request:
```bash
GET /api/task/1
```

**Response**
```json
      {
        "id": 1,
        "title": "Updated Task Title",
        "description": "Updated task description.",
        "priority": "HIGH",
        "status": "IN_PROGRESS",
        "due_date": "2025-03-15",
        "created_by": "id": 1,
        "assigned_to": "id": 2,
        "created_at": "2025-03-01T12:00:00Z",
        "updated_at": "2025-03-01T15:00:00Z"
      }
```

#### Description:
This endpoint is to update the all field of task by  `id`.

#### Example Request:
```bash
PUT /api/task/1
```

**Request body **
```json
      { 
        "title": "Updated Task Title",
        "description": "Updated task description.",
        "priority": "HIGH",
        "status": "IN_PROGRESS",
        "due_date": "2025-03-15",
        "created_by": "id": 1,
        "assigned_to": "id": 2,
       
      }
```
**Response**
```json
      {
        "id": 1,
        "title": "Updated Task Title",
        "description": "Updated task description.",
        "priority": "HIGH",
        "status": "IN_PROGRESS",
        "due_date": "2025-03-15",
        "created_by": "id": 1,
        "assigned_to": "id": 2,
        "created_at": "2025-03-01T12:00:00Z",
        "updated_at": "2025-03-01T15:00:00Z"
      }
```

#### Description:
This endpoint updtae few details for a specific task by its `id`.

#### Example Request:
```bash
patch /api/task/1
```

**Request body **
```json
      { 
        "title": "Updated Task Title",
       
        "priority": "HIGH",
        "status": "IN_PROGRESS",
        "due_date": "2025-03-15",
        "assigned_to": "id": 2,
       
      }
```
**Response**
```json
      {
        "id": 1,
        "title": "Updated Task Title",
        "description": "Updated task description.",
        "priority": "HIGH",
        "status": "IN_PROGRESS",
        "due_date": "2025-03-15",
        "created_by": "id": 1,
        "assigned_to": "id": 2,
        "created_at": "2025-03-01T12:00:00Z",
        "updated_at": "2025-03-01T15:00:00Z"
      }
```

#### Description:
This endpoint delete task by its `id`.

#### Example Request:
```bash
DELETE /api/task/1
```

**Request body **

**Response**
```json
      {

      }
```

### 4. API Endpoint: **GET** `/api/task-report-insight/`

#### Description:
This endpoint provides insight details for all tasks. It utilizes a multi-threaded approach to efficiently generate and prepare task reports. This allows for a faster processing time when working with a large number of tasks.

The insights generated by this endpoint can include task statistics, completion rates, overdue tasks, and other useful analytics based on your tasks data.


#### Example Request:
```bash
GET /api/task-report-insight/
```

**Response**
```json
     {
  "total": 150,
  "completed": 50,
  "pending": 30,
  "tasks_by_priority": {
    "LOW": 40,
    "MEDIUM": 60,
    "HIGH": 30,
    "URGENT": 20
  },
  "tasks_by_status": {
    "PENDING": 30,
    "IN_PROGRESS": 50,
    "COMPLETED": 50,
    "ARCHIVED": 20
  },
  "tasks_assigned": {
    "user1": 40,
    "user2": 30,
    "user3": 50,
    "user4": 20
  },
  "tasks_created": {
    "user1": 50,
    "user2": 40,
    "user3": 30,
    "user4": 30
  },
  "tasks_due_soon": 10
}

```
### 5. Celery Setup and Scheduled Tasks

#### Description:
In this project, we use **Celery** for asynchronous task management, which allows us to run background tasks such as sending notifications without blocking the main application. Celery is combined with **Celery Beat** for scheduling periodic tasks.

#### Setting up Celery and Celery Beat:
1. **Celery Configuration**:  
   We configure Celery to handle asynchronous tasks in the background. Celery Beat is used to schedule tasks periodically.

2. **Scheduled Task Example**:  
   In this example, we are scheduling a task to send notifications every day at **10:00 AM**.

#### Example Celery Beat Schedule Configuration:
```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send_notifications_at_10_am': {
        'task': 'task.tasks.send_due_task_notifications',
        'schedule': crontab(hour=10, minute=0),  # Trigger every day at 10:00 AM
    },
}
```

### 6. Email Notifications for Task Creation and Updates

#### Description:
In this project, we send **email notifications** to users whenever a task is created or updated. The email is sent with a custom **HTML template** located at `templates/task/task_email.html`. 

These notifications keep the users informed about the status of their tasks, ensuring that they are aware of any changes.

#### Email Notification Flow:
1. **Task Created**:  
   When a new task is created, an email notification is sent to the assigned user informing them about the task details.
   
2. **Task Updated**:  
   Whenever a task is updated (e.g., its status or due date is modified), an email notification is sent to the assigned user with the updated task information.

#### Example Email Notification (HTML Template):

- The email notification is rendered using a custom HTML template located at: `templates/task/task_email.html`


### 7. Real-Time Task Updates with WebSockets

#### Description:
The **WebSocket** feature provides real-time updates to the users whenever a task is created, updated, or deleted. This allows the users to stay up-to-date with task changes without needing to refresh the page. The WebSocket connection sends real-time task updates to connected clients.

#### How It Works:
- The WebSocket server listens on a specific endpoint for incoming connections.
- Whenever a task is created, updated, or deleted, the server sends the latest task information to all connected clients. This ensures that all users see the updated task details immediately.

#### WebSocket URL:
The WebSocket connection is established on the following URL:

```bash
    ws://localhost:8001/ws/tasks/
```


- **URL**: `ws://localhost:8001/ws/tasks/`  
- **Protocol**: WebSocket
- **Method**: `CONNECT` (WebSocket handshake)

#### How to Connect to the WebSocket:
1. You need a WebSocket client (e.g., a web browser, WebSocket client library, etc.) to establish a connection.
2. Use the following JavaScript code to connect to the WebSocket and listen for task updates:

```javascript
const socket = new WebSocket('ws://localhost:8001/ws/tasks/');

// Listen for messages from the server
socket.onmessage = function(event) {
  const taskData = JSON.parse(event.data);
  console.log('New task update:', taskData);

  // Handle the task data (you can update the UI here)
  // Example:
  // - Update the task list
  // - Show a notification
};

// Error handling
socket.onerror = function(error) {
  console.error('WebSocket Error:', error);
};

// Closing the connection
socket.onclose = function() {
  console.log('WebSocket connection closed');
};
```


#### How to Connect to WebSocket Using Postman:
1. Open **Postman**.
2. Create a new request by clicking the **New** button and selecting **WebSocket Request**.
3. Enter the following WebSocket URL in the Postman URL field:
```bash
    ws://localhost:8001/ws/tasks/
```

4. Click **Connect** to establish the WebSocket connection.

#### Sending and Receiving WebSocket Messages:
Once the WebSocket connection is established, you will be able to send and receive messages.

- **To send a message**: 
- Use the **Send Message** field to send data if needed. For example, you might send a test task update.
- Typically, the server will push messages automatically when there are task updates (creation, updates, deletions).

- **To receive messages**: 
- Postman will display incoming WebSocket messages in real time in the response area.

#### Example WebSocket Message (Server to Client):
The server sends the following JSON message when a task is created or updated:

```json
{
"task_id": 1,
"title": "Complete the project documentation",
"description": "Write and finalize the project documentation",
"priority": "HIGH",
"status": "IN_PROGRESS",
"due_date": "2025-03-30",
"assigned_to": 2,
"created_at": "2025-03-17T10:00:00Z",
"updated_at": "2025-03-17T10:00:00Z"
}
```


### Key Points to Include in Postman Setup:

1. **WebSocket Request**: In Postman, make sure to create a **WebSocket** request type, not a regular HTTP request.
2. **Connect to WebSocket**: After entering the WebSocket URL (e.g., `ws://localhost:8001/ws/tasks/`), click on **Connect** to establish the connection.
3. **Automatic Updates**: Postman will display incoming messages in real time. You will not need to refresh the connection for the WebSocket to send data; it happens automatically as tasks are created, updated, or deleted.

This section will explain to users how they can test the WebSocket feature using Postman and track real-time task updates while ensuring the WebSocket connection is working correctly.


