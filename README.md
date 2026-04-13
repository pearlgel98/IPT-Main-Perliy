# 🛡️ Connectly API: Secure Micro-Blogging Backend

## 🚀 Project Overview
Connectly is a production-ready RESTful API built with **Django** and **DRF**. It features a decoupled architecture where business logic is handled via design patterns and data access is strictly governed by token-based authentication.

---

## 🏗️ Architectural Design Patterns
To ensure scalability and separation of concerns, the following patterns were implemented:

### 1. Singleton Pattern (`APISettings`)
* **Purpose:** Ensures a single, global point of configuration for API constraints.
* **Function:** Manages system-wide limits (e.g., `max_content_length = 500`) to prevent memory waste and ensure data consistency.

### 2. Factory Pattern (`PostFactory`)
* **Purpose:** Decouples object instantiation from the View layer.
* **Function:** Centralizes the creation logic for `Post` objects. The View layer delegates creation to the Factory, which performs validation against the Singleton settings before saving to the database.

---

## 🔒 Security & Data Integrity
The system employs a multi-layered security approach:

* **Token Authentication:** All endpoints are protected via `TokenAuthentication`. Anonymous requests are rejected with a `401 Unauthorized` status.
* **Object-Level Access Control:** Custom logic in the `PUT` and `DELETE` methods ensures that users can only modify or remove content they personally authored.
* **Automatic Author Attribution:** To prevent identity spoofing, the `author` field is assigned automatically by the backend via the request token, rather than trusting client-side input.

---

## 🛠️ Functional Summary (API Endpoints)

| Method | Endpoint | Security | Design Pattern Involved | Expected Status |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/posts/` | Token Required | N/A | `200 OK` |
| **POST** | `/posts/` | Token Required | **Factory & Singleton** | `201 Created` |
| **PUT** | `/posts/<id>/` | **Owner Only** | N/A | `200 OK` |
| **DELETE** | `/posts/<id>/` | **Owner Only** | N/A | `204 No Content` |

---

## 🧪 Testing Procedures
The API was rigorously tested using **Postman**. Testing included:
1. **Validation Testing:** Sending content over 500 characters to trigger Singleton-based rejection (`400 Bad Request`).
2. **Security Testing:** Attempting unauthorized deletions to verify 403 Forbidden responses.
3. **Lifecycle Testing:** Verified the full CRUD flow from creation to deletion.
# Connectly Social Media API

**Project Overview:** Connectly is a robust, Django-based RESTful API designed for social media interactions. It implements advanced software design patterns, including the **Factory** and **Singleton** patterns, to ensure a scalable and secure architecture for managing users, posts, comments, and likes.

---

## 🤖 AI Disclosure & Collaboration
This project was developed with the assistance of AI (Gemini). The AI’s involvement was strictly limited to:
* **Documentation Assistance:** Formatting technical requirements and refining the project's README and API documentation.
* **Troubleshooting:** Debugging complex environment issues, specifically related to Git branch management and Django Internal Server Errors (500).
* **Code Review:** Providing feedback on best practices for Role-Based Access Control (RBAC) and performance optimization (N+1 query resolution).

**The core logic, database architecture, and security protocols were designed and implemented by the primary developer.**

---

## 🚀 Key Features & API Functions

### 1. Advanced News Feed
* **Endpoint:** `GET /posts/feed/`
* **Logic:** Features reverse-chronological sorting (`-created_at`) and `PageNumberPagination`.
* **Optimization:** Employs `select_related('author')` to optimize database hits and prevent N+1 query issues.

### 2. Role-Based Access Control (RBAC) & Privacy
* **Logic:** Implemented strict data visibility rules using Django `Q` objects.
* **Filtering:** Users can only view "Public" posts or posts they authored.
* **Admin Override:** Staff members have full visibility across all post resources for administrative oversight.

### 3. Factory Design Pattern
* **Service Layer:** All post, comment, and like creation logic is abstracted into a `PostFactory` class.
* **Benefit:** Decouples the API views from the database models, ensuring consistent object instantiation.

### 4. Singleton Pattern Integration
* **Global Constraints:** A Singleton configuration object enforces global business rules, such as character limits for post content, across the entire application.

### 5. Dynamic Engagement Metrics (Like Count)
* **Logic:** Uses a `SerializerMethodField` in the Serializer to calculate like counts in real-time.
* **Performance:** Instead of storing a redundant integer, the API performs an optimized SQL `COUNT` on the related `Like` model.

### 6. Social Interaction Toggle
* **Endpoint:** `POST /posts/<id>/like/`
* **Logic:** A smart toggle function that automatically creates a "Like" relationship if it doesn't exist, or removes it (Unlike) if it does.

### 7. Commenting System (Weak Entity Logic)
* **Endpoint:** `POST /posts/<id>/comments/`
* **Logic:** Handles relational integrity between posts and comments, ensuring comments are correctly mapped as weak entities to the parent post.

---

## 🛠 Tech Stack
* **Backend:** Django & Django Rest Framework (DRF)
* **Database:** SQLite (Development)
* **Patterns:** Factory, Singleton, RBAC
* **Testing:** Postman (with automated pre-request and test scripts)

## 🔗 Task Management API Integration

This project integrates an external Task Management API into the Connectly application.

### 📌 Features Implemented

#### 1. Display Tasks on User Profile
- Fetches tasks from the Task Management API
- Displays tasks associated with the logged-in user
- Ensures only user-specific tasks are shown

#### 2. Share Tasks as Posts
- Allows users to share task details as Connectly posts
- Task data is retrieved from the Task API and formatted as a post

### 🔄 Integration Approach

- Connectly communicates with the Task API using HTTP requests
- APIs remain independent but connected through service calls
- Authentication ensures only authorized users can access tasks

---

### 🧪 Testing

The integration was tested using Postman:
- Verified task retrieval from Task API
- Tested sharing tasks as posts
- Checked proper user-task association
- Validated error handling

---

### ⚠️ Challenges & Solutions

- **Challenge:** OAuth token expiration  
  **Solution:** Ensured code is used immediately after generation  

- **Challenge:** API communication between two services  
  **Solution:** Used consistent endpoints and proper request handling  

- **Challenge:** User-task mapping  
  **Solution:** Matched users using email from Google OAuth  

