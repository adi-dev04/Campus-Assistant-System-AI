# 🎓 Campus Assistant System-(AI)

A web-based **Campus Assistant System** developed using Python and Django to simplify academic resource management and improve communication between students and teachers.

The platform provides a centralized place to access study materials, syllabuses, timetables, notices, and other academic documents. It also includes a local AI-powered assistant to help students understand their study materials.

## 🚀 Features

### 👨‍🎓 Student Panel
- Student registration and login.
- Personalized student dashboard.
- Access to uploaded study materials and PDF documents.
- View syllabuses, timetables, and notices.
- Search academic documents.
- Ask questions about uploaded study materials.
- AI-generated answers based on relevant PDF content.

### 👨‍🏫 Teacher Panel
- Secure teacher login.
- Teacher dashboard.
- Upload academic PDF documents.
- Manage study materials.
- Upload syllabuses, timetables, and notices.
- Make academic resources available to students.

### 🤖 AI Study Assistant
- Local AI integration using Ollama.
- Powered by Qwen2.5:3B.
- PDF-based question answering.
- Retrieves relevant content from uploaded documents.
- Provides student-friendly explanations.

### 📄 PDF Management
- Upload and manage PDF documents.
- Extract text from PDFs using PyMuPDF.
- Store extracted content for searching and retrieval.
- Organize documents by subject, semester, and category.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| HTML5 | Page structure |
| CSS3 | Styling and responsive design |
| JavaScript | Frontend interactions |
| Bootstrap | Responsive UI components |
| SQLite | Database |
| PyMuPDF | PDF text extraction |
| Ollama | Local AI model execution |
| Qwen2.5:3B | AI study assistant |

## 📂 Project Modules

- Student Authentication
- Teacher Authentication
- Student Dashboard
- Teacher Dashboard
- Study Material Management
- PDF Upload and Text Extraction
- Document Search
- Syllabus Management
- Timetable Management
- Notice Management
- AI Study Assistant

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/adi-dev04/Campus-Assistant-System.git
```

### 2. Navigate to the project directory

```bash
cd Campus-Assistant-System
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Run the development server

```bash
python manage.py runserver
```

### 8. Open in your browser

```text
http://127.0.0.1:8000/
```

**Note:** The AI Study Assistant requires Ollama and the Qwen2.5:3B model to be installed and running locally.

## 📸 Screenshots

Add screenshots of your project here.

- Home Page
- Student Login
- Student Dashboard
- Teacher Dashboard
- Study Materials
- Timetable
- AI Study Assistant

## 🎯 Project Objective

The main objective of this project is to develop a centralized academic platform where students can easily access educational resources and teachers can efficiently manage and share academic documents.

## 👨‍💻 Developer

**Aditya Jagtap**

GitHub: [adi-dev04](https://github.com/adi-dev04)

---

⭐ If you find this project useful, consider giving it a star!
