# Connectly Project - Advanced Django REST API

This project is a high-level Social Media REST API built using **Django** and **Django REST Framework (DRF)**. It emphasizes the practical application of software design patterns and secure API architecture.

---

## 🤖 AI Disclosure
**Note on Development:** This project was developed by the author with technical assistance from Gemini (AI). The AI served as a support tool for brainstorming design pattern structures and troubleshooting specific syntax errors. The author remains responsible for the final architecture, logic integration, and manual testing of all API endpoints.

---

## 🚀 Key Features
* **Post & Comment System**: Full CRUD for posts with nested commenting.
* **Smart Like Logic**: A single toggle endpoint to handle both liking and unliking.
* **Design Pattern Integration**: Decoupled logic using Factory and Singleton patterns.
* **Security**: Token-based authentication and strict object-level permissions.

---

## 🛠 Design Patterns Implemented

### 1. Singleton Pattern
* **Location**: `posts/services.py` → `class APISettings`
* **Purpose**: Manages global API configuration in a single, immutable instance.
* **Implementation**: Used to define and enforce global limits like `MAX_POST_LENGTH`.
* **Verification**: The "Singleton Pattern Create" request in the Postman collection demonstrates this pattern blocking requests that exceed the limit.



### 2. Factory Pattern
* **Location**: `posts/services.py` → `class PostFactory`
* **Purpose**: Centralizes and abstracts the creation of `Post` and `Comment` objects.
* **Implementation**: The View layer delegates object creation to `create_post()` and `create_comment()`.
* **Benefit**: Simplifies the Views and ensures that any change in creation logic only needs to be updated in one place.



---

## 📂 Architecture Overview

### Models
* **Post**: The core entity for user content.
* **Comment**: Linked to both a `User` and a `Post`.
* **Like**: Uses a `unique_together` constraint to ensure a user can only like a post once.

### Permissions & Security
* **Authentication**: Uses `rest_framework.authentication.TokenAuthentication`.
* **Permissions**: Implemented `IsAuthenticated` for creation and custom logic to ensure only authors can **Update** or **Delete** their own content.

---

## 🧪 Testing with Postman
A pre-configured Postman collection is included: `Connectly_API.postman_collection.json`.

### Setup Instructions:
1. **Import** the JSON into Postman.
2. Under the Collection **Authorization** tab:
   * **Type**: `API Key`
   * **Key**: `Authorization`
   * **Value**: `Token f72bf666c747b0f27b12eab71d7717e7ffd4965f`
3. **Requests included**:
   * `Create Post` (Factory Verification)
   * `Create Comment` (Nested Logic Verification)
   * `Singleton Pattern Create` (Constraint Verification)
   * `Update/Delete` (Permissions Verification)
