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
