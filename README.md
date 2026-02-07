# 🛡️ Connectly API: Secure Micro-Blogging Backend

## 🚀 Project Overview
A robust RESTful API built with **Django** and **Django Rest Framework (DRF)**. This project demonstrates advanced backend architecture, including token-based authentication, object-level security, and the integration of software design patterns.

---

## 🏗️ Architectural Design Patterns

To meet professional software engineering standards, the system incorporates the following patterns:

### 1. Singleton Pattern
Ensures a single instance of API configuration exists across the application lifecycle.
* **Implementation:** The `APISettings` class manages global constraints (like max character limits) ensuring consistent state across all requests.

### 2. Factory Pattern
Decouples the creation of objects from the view logic.
* **Implementation:** The `PostFactory` handles the instantiation of `Post` objects. This allows for centralized validation and logging before data is committed to the database.

---

## 🔒 Security Implementation

### Authentication & Authorization
* **Token Validation:** All requests require an `Authorization: Token <key>` header.
* **Access Control:** Implemented `IsAuthenticated` to block anonymous traffic.
* **Object-Level Security:** A logic gate ensures that only the original author can `UPDATE` or `DELETE` a specific post.

### Data Integrity
* **Automated Author Mapping:** The `author` field is read-only for the client. The server extracts the user identity directly from the validated token, preventing identity spoofing.

---

## 🛠️ API Endpoints & Testing

| Method | Endpoint | Description | Expected Status |
| :--- | :--- | :--- | :--- |
| **GET** | `/posts/` | Retrieve all posts | 200 OK |
| **POST** | `/posts/` | Create a new post | 201 Created |
| **PUT** | `/posts/<id>/` | Update an owned post | 200 OK |
| **DELETE** | `/posts/<id>/` | Remove an owned post | 204 No Content |

---

## 📋 Installation & Setup
1. **Clone the repo:** `git clone <repo-url>`
2. **Install dependencies:** `pip install django djangorestframework`
3. **Migrate Database:** `python manage.py migrate`
4. **Run Server:** `python manage.py runserver`
