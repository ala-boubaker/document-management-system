from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import PyMongoError, DuplicateKeyError
from bson.objectid import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "document_management_system")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=60000,
    connectTimeoutMS=60000,
    socketTimeoutMS=60000
)

db = client[DB_NAME]
collection = db[COLLECTION_NAME]
users_collection = db["users"]

try:
    collection.create_index("document_id", unique=True)
    users_collection.create_index("username", unique=True)
except PyMongoError:
    print("Warning: Could not create indexes.")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.role = user_data.get("role", "user")


@login_manager.user_loader
def load_user(user_id):
    try:
        user_data = users_collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(user_data)
    except (InvalidId, PyMongoError):
        return None

    return None


def validate_document_form(document_id, title, content, category):
    errors = []

    if not document_id:
        errors.append("Document ID is required.")

    if not title:
        errors.append("Title is required.")

    if not content:
        errors.append("Content is required.")

    if not category:
        errors.append("Category is required.")

    if document_id and len(document_id) < 3:
        errors.append("Document ID must be at least 3 characters.")

    if title and len(title) < 3:
        errors.append("Title must be at least 3 characters.")

    if content and len(content) < 10:
        errors.append("Content must be at least 10 characters.")

    if document_id and len(document_id) > 30:
        errors.append("Document ID must be less than 30 characters.")

    if title and len(title) > 100:
        errors.append("Title must be less than 100 characters.")

    if category and len(category) > 50:
        errors.append("Category must be less than 50 characters.")

    return errors


def user_can_modify(document):
    if current_user.role == "admin":
        return True

    return document.get("created_by") == current_user.id


@app.route("/")
@login_required
def index():
    try:
        sort_by = request.args.get("sort_by", "created_at")
        order = request.args.get("order", "desc")
        page = int(request.args.get("page", 1))
        per_page = 5

        allowed_sort_fields = [
            "created_at",
            "title",
            "category",
            "author",
            "document_id"
        ]

        if sort_by not in allowed_sort_fields:
            sort_by = "created_at"

        if order not in ["asc", "desc"]:
            order = "desc"

        if page < 1:
            page = 1

        sort_order = DESCENDING if order == "desc" else ASCENDING

        total_documents = collection.count_documents({})
        total_pages = max((total_documents + per_page - 1) // per_page, 1)

        documents = (
            collection.find()
            .sort([(sort_by, sort_order), ("_id", ASCENDING)])
            .skip((page - 1) * per_page)
            .limit(per_page)
        )

        return render_template(
            "index.html",
            documents=documents,
            page=page,
            total_pages=total_pages,
            sort_by=sort_by,
            order=order
        )

    except ValueError:
        flash("Invalid page number.")
        return redirect(url_for("index"))

    except PyMongoError:
        flash("Database error while loading documents.")
        return render_template(
            "index.html",
            documents=[],
            page=1,
            total_pages=1,
            sort_by="created_at",
            order="desc"
        )


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_document():
    if request.method == "POST":
        document_id = request.form.get("document_id", "").strip()
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "").strip()

        errors = validate_document_form(document_id, title, content, category)

        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for("add_document"))

        document = {
            "document_id": document_id,
            "title": title,
            "content": content,
            "category": category,
            "author": current_user.username,
            "created_by": current_user.id,
            "created_at": datetime.now(),
            "updated_at": None
        }

        try:
            collection.insert_one(document)
            flash("Document added successfully.")
            return redirect(url_for("index"))

        except DuplicateKeyError:
            flash("Document ID already exists. Please use a unique ID.")
            return redirect(url_for("add_document"))

        except PyMongoError:
            flash("Database error while adding document.")
            return redirect(url_for("add_document"))

    return render_template("add_document.html")


@app.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_document(id):
    try:
        document = collection.find_one({"_id": ObjectId(id)})
    except InvalidId:
        flash("Invalid document ID.")
        return redirect(url_for("index"))
    except PyMongoError:
        flash("Database error while loading document.")
        return redirect(url_for("index"))

    if not document:
        flash("Document not found.")
        return redirect(url_for("index"))

    if not user_can_modify(document):
        flash("You can only edit your own documents.")
        return redirect(url_for("index"))

    if request.method == "POST":
        document_id = request.form.get("document_id", "").strip()
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "").strip()

        errors = validate_document_form(document_id, title, content, category)

        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for("edit_document", id=id))

        updated_data = {
            "document_id": document_id,
            "title": title,
            "content": content,
            "category": category,
            "updated_at": datetime.now()
        }

        try:
            result = collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": updated_data}
            )

            if result.matched_count == 0:
                flash("Document not found.")
            else:
                flash("Document updated successfully.")

            return redirect(url_for("index"))

        except DuplicateKeyError:
            flash("Document ID already exists. Please use another ID.")
            return redirect(url_for("edit_document", id=id))

        except InvalidId:
            flash("Invalid document ID.")
            return redirect(url_for("index"))

        except PyMongoError:
            flash("Database error while updating document.")
            return redirect(url_for("edit_document", id=id))

    return render_template("edit_document.html", document=document)


@app.route("/delete/<id>")
@login_required
def delete_document(id):
    try:
        document = collection.find_one({"_id": ObjectId(id)})
    except InvalidId:
        flash("Invalid document ID.")
        return redirect(url_for("index"))
    except PyMongoError:
        flash("Database error while loading document.")
        return redirect(url_for("index"))

    if not document:
        flash("Document not found.")
        return redirect(url_for("index"))

    if not user_can_modify(document):
        flash("You can only delete your own documents.")
        return redirect(url_for("index"))

    try:
        result = collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            flash("Document not found.")
        else:
            flash("Document deleted successfully.")

        return redirect(url_for("index"))

    except InvalidId:
        flash("Invalid document ID.")
        return redirect(url_for("index"))

    except PyMongoError:
        flash("Database error while deleting document.")
        return redirect(url_for("index"))


@app.route("/search")
@login_required
def search_documents():
    query = request.args.get("query", "").strip()

    if len(query) > 100:
        flash("Search query is too long.")
        return redirect(url_for("search_documents"))

    documents = []

    if query:
        try:
            documents = collection.find({
                "$or": [
                    {"document_id": {"$regex": query, "$options": "i"}},
                    {"title": {"$regex": query, "$options": "i"}},
                    {"content": {"$regex": query, "$options": "i"}},
                    {"category": {"$regex": query, "$options": "i"}},
                    {"author": {"$regex": query, "$options": "i"}}
                ]
            }).sort([("created_at", DESCENDING), ("_id", ASCENDING)])

        except PyMongoError:
            flash("Database error while searching documents.")
            documents = []

    return render_template(
        "search.html",
        documents=documents,
        query=query
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for("register"))

        if len(username) < 3:
            flash("Username must be at least 3 characters.")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters.")
            return redirect(url_for("register"))

        role = "admin" if users_collection.count_documents({}) == 0 else "user"

        user = {
            "username": username,
            "password": generate_password_hash(password),
            "role": role,
            "created_at": datetime.now()
        }

        try:
            users_collection.insert_one(user)
            flash(f"Account created successfully. Your role is: {role}")
            return redirect(url_for("login"))

        except DuplicateKeyError:
            flash("Username already exists.")
            return redirect(url_for("register"))

        except PyMongoError:
            flash("Database error while creating account.")
            return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for("login"))

        try:
            user_data = users_collection.find_one({"username": username})

            if user_data and check_password_hash(user_data["password"], password):
                login_user(User(user_data))
                flash("Logged in successfully.")
                return redirect(url_for("index"))

            flash("Invalid username or password.")
            return redirect(url_for("login"))

        except PyMongoError:
            flash("Database error while logging in.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("base.html"), 404


@app.errorhandler(500)
def internal_error(error):
    flash("An unexpected server error occurred.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)