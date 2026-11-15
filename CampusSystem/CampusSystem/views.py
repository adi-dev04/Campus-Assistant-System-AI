from django.core.checks import messages
from django.http import HttpResponse, request
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
import fitz
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama
from django.http import JsonResponse
from .models import PDFDocument
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from CampusSystem.forms import PDFDocumentForm
from CampusSystem.models import CampusSystem
from django.contrib.admin.views.decorators import staff_member_required

def get_pdf_chunks():

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    documents = PDFDocument.objects.all()

    all_chunks = []

    for doc in documents:

        text = doc.extracted_text or ""

        if text.strip():

            chunks = splitter.split_text(text)

            for chunk in chunks:
                all_chunks.append({
                    'text': chunk,
                    'title': doc.title,
                    'category': doc.category,
                    'document_id': doc.id
                })

    return all_chunks

def get_relevant_chunks(question):

    chunks = get_pdf_chunks()

    question_words = set(question.lower().split())

    scored_chunks = []

    for chunk in chunks:

        text = chunk['text'].lower()

        score = sum(
            1 for word in question_words
            if len(word) > 2 and word in text
        )

        if score > 0:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda item: item[0], reverse=True)

    return [chunk for score, chunk in scored_chunks[:3]]

def home(request):
    return render(request, 'Campus/home.html')

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("student_dashboard")

        else:
            messages.error(
                request,
                "Invalid username or password"
            )

    return render(request, "Campus/login.html")

def quiz_view(request):
    questions = [
        {
            "question": "What is Python?",
            "options": ["Browser", "Programming Language", "Database", "OS"],
            "answer": "Programming Language"
        },
        {
            "question": "Which tag creates a heading in HTML?",
            "options": ["<p>", "<h1>", "<br>", "<img>"],
            "answer": "<h1>"
        },
        {
            "question": "Which language is used to style web pages?",
            "options": ["Python", "SQL", "CSS", "Django"],
            "answer": "CSS"
        }
    ]

    score = None

    if request.method == "POST":
        score = 0

        for i, q in enumerate(questions):
            selected = request.POST.get(f"question{i}")

            if selected == q["answer"]:
                score += 1

    return render(request, "Campus/quiz.html", {
        "questions": questions,
        "score": score
    })

def home_view(request):
    return render(request, 'Campus/index.html')

def delete_upload(request, document_id):
    if request.method == "POST":
        document = get_object_or_404(PDFDocument, id=document_id)

        document.file.delete(save=False)
        document.delete()

    return redirect('manage_uploads')


def tlogin_view(request):
    return render(request, 'Campus/tlogin.html')

def student_portal_view(request):
    documents = PDFDocument.objects.all().order_by("-uploaded_at")

    return render(
        request,
        'Campus/studentportal.html',
        {'documents': documents}
    )
def syllabus_view(request):
    syllabus = PDFDocument.objects.filter(
        category="Syllabus"
    ).order_by('-uploaded_at')

    return render(request, 'Campus/syllabus.html', {
        'syllabus': syllabus
    })

def upload_notice(request):
    if request.method == "POST":
        title = request.POST.get('title')
        file = request.FILES.get('file')

        if file:
            document = PDFDocument.objects.create(
                title=title,
                subject="General",
                semester="All",
                category="Notice",
                academic_year="2026-27",
                file=file
            )

            extract_pdf_text(document)

            return redirect('home')

    return render(request, 'Campus/upload_notice.html')

def notice_view(request):

    notices = PDFDocument.objects.filter(
        category="Notice"
    ).order_by('-uploaded_at')

    return render(request, 'Campus/notice.html', {
        'notices': notices
    })

def upload_timetable(request):
    if request.method == "POST":
        title = request.POST.get('title')
        file = request.FILES.get('file')

        if file:
            document = PDFDocument.objects.create(
                title=title,
                subject="General",
                semester="All",
                category="Timetable",
                academic_year="2026-27",
                file=file
            )

            extract_pdf_text(document)

            return redirect('home')

    return render(request, 'Campus/upload_timetable.html')
def timetable_view(request):

    timetable = PDFDocument.objects.filter(
        category="Timetable"
    ).order_by('-uploaded_at')

    timetable_data = []

    for doc in timetable:
        print("PDF TITLE:", doc.title)
        print("EXTRACTED TEXT:", doc.extracted_text)

        rows = extract_timetable(doc.extracted_text or "")

        timetable_data.append({
            'title': doc.title,
            'rows': rows,
            'uploaded_at': doc.uploaded_at,
            'file': doc.file.url
        })

    return render(request, 'Campus/timetable.html', {
        'timetable_data': timetable_data
    })
def manage_uploads(request):
    documents = PDFDocument.objects.all().order_by('-uploaded_at')

    return render(request, 'Campus/manage_uploads.html', {
        'documents': documents
    })


@staff_member_required
def upload_pdf(request):
    if request.method == "POST":
        form = PDFDocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save()

            try:
                with fitz.open(document.file.path) as pdf:
                    text = ""

                    for page in pdf:
                        text += page.get_text() + "\n"

                document.extracted_text = text
                document.save(update_fields=["extracted_text"])

                messages.success(
                    request,
                    "PDF uploaded and text extracted successfully!"
                )
                return redirect("upload_pdf")

            except Exception:
                document.delete()
                messages.error(
                    request,
                    "Could not read this PDF. Please upload a valid PDF."
                )

    else:
        form = PDFDocumentForm()

    return render(
        request,
        "Campus/upload_pdf.html",
        {"form": form},
    )


import fitz
from .models import PDFDocument

def extract_pdf_text(document):
    if document.file:
        try:
            with fitz.open(document.file.path) as pdf:
                text = "\n".join(
                    page.get_text() for page in pdf
                )

            document.extracted_text = text

            sentences = [
                s.strip()
                for s in text.replace("\n", " ").split(".")
                if len(s.strip()) > 30
            ]

            document.summary = ". ".join(sentences[:5])

            document.save(
                update_fields=["extracted_text", "summary"]
            )

        except Exception as e:
            print("PDF extraction error:", e)




def student_documents(request) -> HttpResponse:
    query = request.GET.get('q', '').strip()

    documents = PDFDocument.objects.all().order_by('-uploaded_at')

    if query:
        documents = documents.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query) |
            Q(category__icontains=query) |
            Q(academic_year__icontains=query) |
            Q(extracted_text__icontains=query)
        )
        for doc in documents:
            text = doc.extracted_text or ""
            if query:
                index = text.lower().find(query.lower())
                if index != -1:
                    start = max(0, index - 100)
                    end = min(len(text), index + len(query) + 150)
                    snippet = text[start:end]
                    doc.matching_text = re.sub(
                        re.escape(query),
                        lambda match: f"<mark>{match.group()}</mark>",
                        snippet,
                        flags=re.IGNORECASE
                    )

    return render(request, 'Campus/studentdoc.html', {
        'documents': documents,
        'query': query
    })



def document_detail(request, document_id):
    document = get_object_or_404(PDFDocument,id=document_id,
    )

    return render(
        request,
        "Campus/docdetail.html",
        {"document": document},
    )




def upload_syllabus(request):
    if request.method == "POST":
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        semester = request.POST.get('semester')
        academic_year = request.POST.get('academic_year')
        file = request.FILES.get('file')

        if file:
            document = PDFDocument.objects.create(
                title=title,
                subject=subject,
                semester=semester,
                category="Syllabus",
                academic_year=academic_year,
                file=file
            )

            extract_pdf_text(document)

            return redirect('home')

    return render(request, 'Campus/upload_pdf.html')


import ollama
from django.http import HttpResponse

def test_qwen(request):
    response = ollama.chat(
        model='qwen2.5:3b',
        messages=[
            {
                'role': 'user',
                'content': 'Explain Python inheritance in simple words.'
            }
        ]
    )

    answer = response['message']['content']

    return HttpResponse(answer)

def ask_qwen(request):

    ai_answer = ""

    if request.method == "POST":

        question = request.POST.get('question', '').strip()

        if question:

            relevant_chunks = get_relevant_chunks(question)
            print("STUDENT QUESTION:", question)
            print("RETRIEVED CHUNKS:")
            for chunk in relevant_chunks:
                print("PDF TITLE:", chunk['title'])
                print("PDF CONTENT:", chunk['text'])
                print("-------------------")

            pdf_context = ""

            for chunk in relevant_chunks:
                pdf_context += (
                    f"\nDocument: {chunk['title']}\n"
                    f"Category: {chunk['category']}\n"
                    f"Content: {chunk['text']}\n"
                )

            if pdf_context:
                system_prompt = f"""
                You are a supportive college study assistant.
                Use the following uploaded PDF content when it is
                relevant to the student's question:
                {pdf_context}
                Prioritize information from these documents.
                Do not invent information or claim something is
                present in a PDF if it is not.
                Explain concepts clearly and simply.
                """
            else:
                system_prompt = """
                You are a knowledgeable and supportive study assistant.
                No relevant information was found in the uploaded PDFs.
                Answer the student's question using your own general
                knowledge.
                Explain clearly and simply, and provide examples when useful.
                Never refuse just because information is unavailable in PDFs.
                """

# COMMON FORMATTING INSTRUCTIONS
        system_prompt += """
           STRICT TIMETABLE TABLE FORMAT:
           When answering timetable questions, follow this exact format:
           | TIME | MONDAY | TUESDAY | WEDNESDAY | THURSDAY | FRIDAY |
           |---|---|---|---|---|---|
           | 09:00 - 10:00 AM | Mathematics, Room 101 | Physics, Lab 2 | Mathematics, Room 101 | History, Room 204 | Biology, Lab 1 |
           IMPORTANT RULES:
           1. Every row MUST contain exactly 6 cells.
           2. Never create additional columns.
           3. Never use the | character inside a cell.
           4. Keep subject and room together in the same cell.
           5. Each time slot must occupy exactly one row.
           6. Use - for empty cells.
           7. Never invent or rearrange subjects.
           8. Use the uploaded PDF as the source of truth.
           9. Include all available timetable entries.
           10. Return only the Markdown table, without separate weekday lists.
           print the table exactly as shown above, with no extra text or explanation.
           print in white text only.
           """
        response = ollama.chat(
            model='qwen2.5:3b',
            messages=[
                {
                    'role': 'system',
                    'content': system_prompt
                    },
                    {
                        'role': 'user',
                        'content': question
                        }
                        ]
                        )
        ai_answer = response['message']['content']
        documents = PDFDocument.objects.all().order_by('-uploaded_at')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'answer': ai_answer})
        return render(request, 'Campus/studentdoc.html', {
                'documents': documents,
                'ai_answer': ai_answer
                })

def extract_timetable(pdf_text):

    lines = [
        line.strip()
        for line in pdf_text.splitlines()
        if line.strip()
    ]

    timetable = []

    i = 0

    while i < len(lines):

        # Identify time slot
        if re.match(
            r'^\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}\s*(AM|PM)$',
            lines[i],
            re.IGNORECASE
        ):

            time = lines[i]
            row = [time]

            i += 1

            # Extract 5 days
            for day in range(5):

                if i + 1 < len(lines):

                    subject = lines[i]
                    room = lines[i + 1]

                    row.append(subject + "\n" + room)

                    i += 2

            if len(row) == 6:
                timetable.append(row)

        else:
            i += 1

    return timetable[:5]




