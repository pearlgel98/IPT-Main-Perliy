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


1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Mitchy3002/IPT-Main.git](https://github.com/Mitchy3002/IPT-Main.git)
