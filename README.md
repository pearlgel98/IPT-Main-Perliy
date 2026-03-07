# Connectly API - Design Pattern Implementation

This document outlines the custom architectural enhancements made to the Connectly project, focusing on Creational Design Patterns and advanced API logic.

---

## 🤖 AI Disclosure
**Note on Development:** This project was developed with the assistance of an AI collaborator (Gemini). AI served as a peer-programming tool to help structure Design Patterns and debug complex serializer logic. The final implementation, architectural review, and manual verification were performed by the author.

---

## 🛠 Custom Design Patterns

### 1. Singleton Pattern (Configuration Management)
* **File**: `posts/services.py` → `class APISettings`
* **Implementation**: A thread-safe Singleton that manages global application limits.
* **Reasoning**: Ensures that the API character limits are consistent across all views and services without redundant database calls or hard-coded strings.
* **Verification**: Tested via Postman; sending a post body exceeding the `MAX_POST_LENGTH` triggers a `400 Bad Request`.



### 2. Factory Pattern (Object Creation)
* **File**: `posts/services.py` → `class PostFactory`
* **Implementation**: Centralized creation logic for `Post` and `Comment` objects.
* **Reasoning**: Decouples the View layer from the Model layer. This abstraction allows for additional logic (like auto-tagging or notifications) to be added in the future without modifying the View code.
* **Verification**: All `POST` requests in the Postman collection utilize this factory for object instantiation.



---

## 📂 Logic & Security Enhancements

### 💬 Nested Commenting System
* Implemented a relationship-aware `Comment` model linked to `Post`.
* **Serializer Logic**: Updated `PostSerializer` to include a nested `comments` array, providing a complete data tree in a single `GET` request.

### ❤️ Smart Like Toggle
* **Endpoint**: `POST /posts/{id}/like/`
* **Logic**: Instead of separate like/unlike endpoints, a custom action was created in the ViewSet. It checks for the existence of a `Like` object: if it exists, it deletes it (unlike); if not, it creates it (like).

### 🔒 Author-Only Permissions
* Beyond basic authentication, custom permission logic was applied to `Update` and `Delete` actions. 
* **Rule**: While any authenticated user can view posts, only the `author` has the authority to modify or remove them.

---

## 🧪 Postman Verification
The included `Connectly_API.postman_collection.json` specifically tests the custom logic above:
1.  **Factory Check**: `Create Post` & `Create Comment`.
2.  **Singleton Check**: `Singleton Pattern Create` (triggers limit validation).
3.  **Security Check**: `Update` & `Delete` (verifies author-level access).
