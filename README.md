# 📚 Document Management System

A secure and scalable **Document Management System (DMS)** developed using **Flask** and **MongoDB Atlas**. The system allows users to create, search, update, and manage documents while enforcing authentication and role-based authorization.

---

## 🚀 Project Overview

This project was developed as part of a Big Data and NoSQL course to demonstrate the integration of:

* Flask Web Framework
* MongoDB Atlas Cloud Database
* User Authentication & Authorization
* CRUD Operations
* Search & Filtering
* Pagination & Sorting
* Data Validation
* Error Handling
* Git & GitHub Version Control

The application provides a secure environment where users can manage documents according to their assigned permissions.

---

## ✨ Features

### Authentication

* User Registration
* User Login
* User Logout
* Secure Password Hashing

### Authorization

#### Administrator

* View all documents
* Create documents
* Edit any document
* Delete any document
* Search all documents

#### Regular User

* View all documents
* Search all documents
* Create documents under their own username
* Edit only their own documents
* Delete only their own documents

---

## 📂 Document Management

Each document contains:

| Field       | Description                 |
| ----------- | --------------------------- |
| Document ID | Unique document identifier  |
| Title       | Document title              |
| Content     | Main document content       |
| Category    | Document category           |
| Author      | Creator of the document     |
| Created At  | Creation timestamp          |
| Updated At  | Last modification timestamp |

---

## 🛠 Technologies Used

### Backend

* Python 3.x
* Flask
* PyMongo
* Werkzeug Security

### Database

* MongoDB Atlas

### Frontend

* HTML5
* CSS3
* Jinja2 Templates

### Development Tools

* Visual Studio Code
* Git
* GitHub

---

## 🗄 Database Structure

### Users Collection

```json
{
    "username": "admin",
    "password": "hashed_password",
    "role": "admin"
}
```

### Documents Collection

```json
{
    "document_id": "DOC001",
    "title": "MongoDB Basics",
    "content": "Introduction to MongoDB.",
    "category": "Technology",
    "author": "Alaeddine",
    "created_at": "2025-06-01",
    "updated_at": "2025-06-01"
}
```

---

## 🔒 Security Features

### Password Security

Passwords are never stored in plain text.

```python
generate_password_hash()
check_password_hash()
```

### Session Management

* Login required for protected pages
* Session-based authentication
* Automatic logout support

### Role-Based Access Control

The system verifies user permissions before allowing:

* Edit operations
* Delete operations
* Administrative actions

---

## ⚠ Error Handling & Validation

### Input Validation

* Required fields validation
* Duplicate Document ID prevention
* Empty field detection
* User existence verification

### Error Handling

* Database connection errors
* Invalid document access
* Unauthorized access attempts
* Search exceptions

---

## 🔍 Search Functionality

Users can search documents by:

* Document ID
* Title
* Category
* Author
* Content

MongoDB regular expressions are used to provide flexible searching.

---

## 📄 Pagination & Sorting

### Pagination

Documents are displayed across multiple pages for better performance.

### Sorting Options

* Created Date
* Updated Date
* Title
* Category
* Author

Ascending and descending order are supported.

---

## ⚙ Installation

### Clone Repository

```bash
git clone https://github.com/ala-boubaker/document-management-system.git
```

```bash
cd document-management-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 Environment Variables

Create a `.env` file:

```env
MONGO_URI=your_mongodb_connection_string
DB_NAME=document_management_system
COLLECTION_NAME=documents
```

**Important:** Never upload `.env` files to GitHub.

---

## ▶ Running the Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 📸 Screenshots

Add screenshots of:

* Login Page
* Registration Page
* Dashboard
* Search Results
* MongoDB Atlas Collection

Store them in:

```text
screenshots/
```

Example:

```markdown
![Dashboard](screenshots/dashboard.png)
```

---

## 🧪 Testing

The project includes test data scripts located in:

```text
tests/
```

These scripts can be used to:

* Insert sample documents
* Test CRUD operations
* Validate MongoDB connectivity

---

## 📈 Future Improvements

* File Upload (PDF, DOCX)
* REST API
* Docker Deployment
* User Profile Management
* Audit Logging
* Advanced Search Filters
* Dashboard Analytics
* Email Notifications

---

## 👨‍💻 Author

**Alaeddine Boubaker**

PhD Student – Big Data & NoSQL

GitHub:
https://github.com/ala-boubaker

---

## 📜 License

This project is developed for educational and academic purposes.
