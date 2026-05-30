from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from prompt_toolkit import prompt
from .models import Course, Semester, Subject, Department
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Course, PythonTopic, LectureVideo, CourseFile, Question
from django.core.paginator import Paginator
from .ai import get_final_answer
# Create your views here.


@login_required
def index(request):
    return render(request, 'academics/index1.html')


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'academics/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'academics/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):


# Because it is a DetailView, Django automatically does:
# self.object = Course.objects.get(pk=3)

# This happens BEFORE your get_context_data().
# This is why:

# course = self.object



# If Django passes URL parameters → the function must accept them
# If not → no kwargs needed


# User clicks → Django finds URL → Django fetches course → self.object is ready → I use it to fetch videos, files, topics → page is rendered

        context = super().get_context_data(**kwargs)
        # “Pass the URL parameters (pk=3) to Django’s parent class so it can do its job.”
        # self.object = Course.objects.get(pk=3),  The above code line is reason for this internal happening. 
        course = self.object
        topics_ = PythonTopic.objects.filter(course=course).order_by('id')
        paginator = Paginator(topics_, 20)
        page = int(self.request.GET.get('page', 1))
        topics = paginator.get_page(page)

        for topic in topics:
            if topic.example_code:
            # Strip any leading or trailing empty lines
                lines = topic.example_code.strip().splitlines()
                # Remove spaces from the first actual code line
                if lines:
                    lines[0] = lines[0].lstrip()
                    topic.example_code = "\n".join(lines)

        # Add related topics, videos, and files
        context['topics'] = topics
        context['videos'] = LectureVideo.objects.filter(course=course)
        context['files'] = CourseFile.objects.filter(course=course)

        
        questions = Question.objects.filter(course=course, page_number=page).order_by('id')
        context['questions_page'] = questions
        
        return context

class SubjectList(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'academics/subject_list.html'
    context_object_name = 'subjects'
    
    
    
@login_required
def branch_subject_view(request):
    departments = Department.objects.all()
    selected_id = request.GET.get('branch_id')

    selected_department = None
    semesters = []

    if selected_id:
        selected_department = Department.objects.get(id=selected_id)
        semesters = selected_department.semester_set.prefetch_related('subject_set')
        #<model>_set is auto-created by Django for ForeignKey relations
        
        # selected_department.semester_set is equivalent to:
        #     Semester.objects.filter(department=selected_department)

        
        
#         Example from YOUR models

# 🔹 Subject → Semester (ForeignKey)
# subjects = Subject.objects.select_related('semester')
# Because:
# Each Subject has ONE Semester


# 🔹 Semester → Subject (reverse FK)
# semesters = Semester.objects.prefetch_related('subject_set')
# Because:
# Each Semester has MANY Subjects

##Forward FK → select_related
# Reverse FK / many → prefetch_related



# Case 1️⃣: WITHOUT prefetch_related
# semesters = selected_department.semester_set.all()

# What Django does:

# 1 query → fetch all semesters
# 1 query per semester → fetch its subjects
# If you have 5 semesters:
# 1 (semesters) + 5 (subjects) = 6 queries


# This is called the N+1 query problem.

#  Correct result
#  Slower as data grows

    return render(request, 'academics/branch_subjects.html', {
        'departments': departments,
        'selected_department': selected_department,
        'semesters': semesters
    })


# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from groq import Groq
# import os

# # Initialize Groq client once
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# @csrf_exempt
# def ask_gemini(request):   # keep SAME name (important)

#     #  PAGE LOAD
#     if request.method == "GET":
#         return render(request, "academics/ai.html")

#     # AI CHAT
#     if request.method == "POST":
#         try:
#             prompt = request.POST.get("prompt", "").strip()

#             if not prompt:
#                 return JsonResponse({"response": "Please type something."})

#             #  GROQ AI RESPONSE
#             response = client.chat.completions.create(
#                 model="llama-3.1-8b-instant",
#                 messages=[
#                     {
#                         "role": "system",
#                         "content": "You are AI-Tutor, a helpful programming tutor. Explain clearly with examples when needed."
#                     },
#                     {
#                         "role": "user",
#                         "content": prompt
#                     }
#                 ],
#                 temperature=0.3,
#                 max_tokens=700
#             )

#             ai_text = response.choices[0].message.content

#             return JsonResponse({
#                 "response": ai_text
#             })

#         except Exception as e:
#             print("GROQ ERROR:", e)
#             return JsonResponse(
#                 {"response": "⚠️ AI service error"},
#                 status=500
#             )

#     return JsonResponse({"error": "Method not allowed"}, status=405)



from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from langchain_community.chat_models import ChatOllama

from langchain_core.messages import HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.chains import RetrievalQA

from tavily import TavilyClient

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')


import tempfile
import os


# =========================
# OLLAMA MODEL
# =========================

model = ChatOllama(
    model="gemma3:1b",
    temperature=0.3
)


# =========================
# WEB SEARCH
# =========================

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


# =========================
# MEMORY STORE
# =========================

store = {}

# USER PDF VECTOR STORE
user_vectors = {}


# =========================
# GET USER MEMORY
# =========================

def get_session_history(session_id: str) -> BaseChatMessageHistory:

    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    return store[session_id]


# =========================
# MEMORY WRAPPER
# =========================

with_message_history = RunnableWithMessageHistory(
    model,
    get_session_history
)


# =========================
# PDF VECTOR CREATION
# =========================

def create_pdf_vectorstore(pdf_file, session_id):

    temp_dir = tempfile.mkdtemp()

    temp_path = os.path.join(temp_dir, pdf_file.name)

    with open(temp_path, "wb+") as f:

        for chunk in pdf_file.chunks():
            f.write(chunk)

    loader = PyPDFLoader(temp_path)

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    split_docs = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    vectorstore = FAISS.from_documents(
        split_docs,
        embeddings
    )

    user_vectors[session_id] = vectorstore


# =========================
# MAIN CHAT VIEW
# =========================

@csrf_exempt
@login_required
def ask_gemini(request):

    # PAGE LOAD
    if request.method == "GET":
        return render(request, "academics/ai.html")


    # =========================
    # USER SESSION
    # =========================

    if request.user.is_authenticated:

        session_id = f"user_{request.user.id}"

    else:

        session_id = request.session.session_key

        if not session_id:
            request.session.create()
            session_id = request.session.session_key


    # =========================
    # PDF UPLOAD
    # =========================

    if request.method == "POST" and request.FILES.get("pdf"):

        try:

            pdf_file = request.FILES["pdf"]

            create_pdf_vectorstore(
                pdf_file,
                session_id
            )

            return JsonResponse({
                "response": "✅ PDF uploaded successfully. You can now chat with the document."
            })

        except Exception as e:

            print("PDF ERROR:", e)

            return JsonResponse({
                "response": "⚠️ PDF processing failed"
            })


    # =========================
    # NORMAL CHAT
    # =========================

    if request.method == "POST":

        try:

            prompt = request.POST.get(
                "prompt",
                ""
            ).strip()

            if not prompt:

                return JsonResponse({
                    "response": "Please type something."
                })


            config = {
                "configurable": {
                    "session_id": session_id
                }
            }


            # =========================
            # WEB SEARCH MODE
            # =========================

            web_keywords = [
                "latest",
                "current",
                "today",
                "news",
                "2026",
                "price",
                "cm",
                "pm",
                "president"
            ]


            use_web = any(
                word in prompt.lower()
                for word in web_keywords
            )


            # =========================
# PDF RAG MODE
# =========================

            if session_id in user_vectors:

                retriever = user_vectors[
                    session_id
                ].as_retriever(search_kwargs={"k": 4})

                docs = retriever.get_relevant_documents(prompt)

                context = "\n\n".join(
                    [doc.page_content for doc in docs]
                )

                final_prompt = f"""
            You are an AI assistant.

            Answer ONLY using the PDF content below.

            If answer is not present in PDF,
            say:
            "I could not find that in the uploaded PDF."

            PDF Content:
            {context}

            User Question:
            {prompt}
            """

            else:

                final_prompt = prompt


            # =========================
            # WEB SEARCH
            # =========================

            if use_web:

                search_result = tavily.search(
                    query=prompt,
                    max_results=3
                )

                web_context = ""

                for result in search_result["results"]:

                    web_context += (
                        result["content"] + "\n"
                    )

                final_prompt += f"""

                Latest web information:
                {web_context}

                Use latest information if relevant.
                """


            # =========================
            # FINAL AI RESPONSE
            # =========================

            response = with_message_history.invoke(
                [
                    HumanMessage(
                        content=final_prompt
                    )
                ],
                config=config
            )

            ai_text = response.content

            return JsonResponse({
                "response": ai_text
            })


        except Exception as e:

            print("OLLAMA ERROR:", e)

            return JsonResponse(
                {
                    "response": "⚠️ AI service error"
                },
                status=500
            )


    return JsonResponse(
        {
            "error": "Method not allowed"
        },
        status=405
    )



# ###### Python Course Model #######
# def python_course(request):
#     # Get the "Python" course or return 404 if not found
#     course = get_object_or_404(Course, name="Python")

#     # Get all topics, videos, and files related to this course
#     topics = PythonTopic.objects.filter(course=course).order_by('id')
#     videos = LectureVideo.objects.filter(course=course)
#     files = CourseFile.objects.filter(course=course)

#     return render(request, 'academics/python.html', {
#         'course': course,
#         'topics': topics,
#         'videos': videos,
#         'files': files,
#     })

######### Compiler(Python) ###############
from django.views.decorators.csrf import csrf_exempt
import requests
import base64
import time
@csrf_exempt
@login_required
def run_code(request):
    context = {}
    if request.method == "POST":
        code = request.POST.get("code", "")
        inp = request.POST.get("inp", "")

        headers = {
            "Content-Type": "application/json",
            "X-RapidAPI-Key": "2289620fd3msh8c3eeaa96f71c18p181243jsn7bcc6fc11399",
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
        }

        payload = {
            "language_id": 71,  # Python 3
            "source_code": base64.b64encode(code.encode()).decode(),
            "stdin": base64.b64encode(inp.encode()).decode()
        }

        # Submit code
        res = requests.post("https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=true&wait=false", headers=headers, json=payload)
        token = res.json().get("token")
        time.sleep(2)

        # Fetch result
        result = requests.get(f"https://judge0-ce.p.rapidapi.com/submissions/{token}?base64_encoded=true", headers=headers).json()

        output = result.get("stdout") or result.get("stderr") or result.get("compile_output") or "No output"
        if output:
            try:
                output = base64.b64decode(output).decode()
            except Exception:
                pass

        # Send data back to template
        context = {
            "output": output,
            "code": code,
            "stdin": inp
        }

    return render(request, "academics/coding_langs/compiler.html", context)

LANGUAGE_IDS = {
    
    "react": 63,
    "python": 71,       # Python 3
    "c": 50,            # C (GCC 9.2.0)
    "cpp": 54,          # C++ (GCC 9.2.0)
    "java": 62,         # Java (OpenJDK 13.0.1)
    "javascript": 63,   # JavaScript (Node.js 12.14.0)
    "nodejs": 63        # Same as JavaScri
}

LANGUAGE_LABELS = {
    "c": "C",
    "python": "Python",
    "javascript": "JavaScript",
    "node": "Node.js",
    "react": "React",
    "cpp": "CPP",
    "java": "Java"
}


DEFAULT_CODE = {
    "python": 'print("Hello, World!")',
    "c": '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
    "cpp": '#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello, World!" << endl;\n    return 0;\n}',
    "javascript": 'console.log("Hello, World!");',
    "nodejs": 'console.log("Hello, Node.js World!");',
    "java": 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
}

@csrf_exempt
@login_required
def run_code_big(request):
    output = ""
    code = ""
    inp = ""
    active_language = "python"

    if request.method == "POST":
        active_language = request.POST.get("language", "python")
        code = request.POST.get("code") or DEFAULT_CODE.get(active_language, "")
        if not code.strip():
            code = DEFAULT_CODE.get(active_language, "")
        inp = request.POST.get("inp", "")
    
        headers = {
            "Content-Type": "application/json",
            "X-RapidAPI-Key": "2289620fd3msh8c3eeaa96f71c18p181243jsn7bcc6fc11399",
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
        }

        payload = {
            "language_id": LANGUAGE_IDS.get(active_language, 71),
            "source_code": base64.b64encode(code.encode()).decode(),
            "stdin": base64.b64encode(inp.encode()).decode()
        }

        # Submit code and wait for result
         # Submit code
        res = requests.post("https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=true&wait=false", headers=headers, json=payload)
        print(res.status_code)   # Should be 200
        print(res.text)   
        token = res.json().get("token")
        time.sleep(2)

        # Fetch result
        result = requests.get(f"https://judge0-ce.p.rapidapi.com/submissions/{token}?base64_encoded=true", headers=headers).json()

        output = result.get("stdout") or result.get("stderr") or result.get("compile_output") or "No output"
        if output:
            try:
                output = base64.b64decode(output).decode()
            except Exception:
                pass
    else:
        code = DEFAULT_CODE.get(active_language, "")
        
    context = {
        "output": output,
        "code": code,
        "active_language": active_language,
        "language_labels": LANGUAGE_LABELS,
        "DEFAULT_CODE": DEFAULT_CODE
    }
    return render(request, "academics/coding_langs/big_compiler.html", context)


@login_required
def ai_architect(request):
    import subprocess
    import os
    from django.contrib import messages
    from django.shortcuts import redirect

    exe_path = r"D:\AntiGravity\AI_Architect_Exe\dist\AI_Architect_v19.exe"
    exe_exists = os.path.exists(exe_path)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'launch':
            if not exe_exists:
                messages.error(request, "AI Architect executable not found on the local path D:\\AntiGravity\\AI_Architect_Exe\\dist\\AI_Architect_v19.exe.")
                return redirect('ai_architect')
            try:
                # Start the executable in a non-blocking background process
                creation_flags = subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
                subprocess.Popen([exe_path], creationflags=creation_flags)
                messages.success(request, "AI Architect launched successfully! Look for the application window on your desktop taskbar.")
            except Exception as e:
                messages.error(request, f"Error launching AI Architect: {str(e)}")
            return redirect('ai_architect')

    context = {
        'exe_exists': exe_exists,
        'download_url': 'https://drive.google.com/file/d/1VvAaE3eZI0s--TShg_fCnolH5StvgdWs/view?usp=sharing'
    }
    return render(request, 'academics/ai_architect.html', context)