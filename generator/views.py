from django.shortcuts import render, redirect
import random
from .questions import questions


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == 'admin123':
            return redirect('home')

        return render(request, 'login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'login.html')


def home(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        branch = request.POST.get('branch')
        semester = request.POST.get('semester')
        academic_year = request.POST.get('academic_year')
        exam_type = request.POST.get('exam_type')
        units = request.POST.get('units')
        marks = request.POST.get('marks')
        difficulty = request.POST.get('difficulty')
        question_type = request.POST.get('question_type')

        # -----------------------------------------
        # READ TOTAL MARKS
        # -----------------------------------------

        try:
            total_marks = int(marks)
        except (ValueError, TypeError):
            total_marks = 30

        # -----------------------------------------
        # FILTER QUESTION BANK
        # -----------------------------------------

        selected_questions = questions.copy()

        # Filter by unit
        if units != "all" and units:
            selected_questions = [
                q for q in selected_questions
                if str(q["unit"]) == str(units)
            ]

        # Filter by difficulty
        if difficulty != "balanced":
            selected_questions = [
                q for q in selected_questions
                if q["difficulty"] == difficulty
            ]

        # Filter by question type
        if question_type != "mixed" and question_type:
            selected_questions = [
                q for q in selected_questions
                if q["type"] == question_type
            ]

        # -----------------------------------------
        # SEPARATE QUESTIONS BY MARKS
        # -----------------------------------------

        section_a_pool = [
            q for q in selected_questions
            if q["marks"] == 2
        ]

        section_b_pool = [
            q for q in selected_questions
            if q["marks"] == 5
        ]

        section_c_pool = [
            q for q in selected_questions
            if q["marks"] == 10
        ]

        # -----------------------------------------
        # QUESTION PAPER PATTERN
        # -----------------------------------------

        if total_marks == 30:

            section_a_count = 5
            section_b_count = 2
            section_c_count = 1

        elif total_marks == 60:

            section_a_count = 5
            section_b_count = 4
            section_c_count = 3

        else:

            # Default pattern for unsupported marks
            section_a_count = 5
            section_b_count = 2
            section_c_count = 1

        # -----------------------------------------
        # CHECK WHETHER ENOUGH QUESTIONS EXIST
        # -----------------------------------------

        if (
            len(section_a_pool) < section_a_count
            or len(section_b_pool) < section_b_count
            or len(section_c_pool) < section_c_count
        ):

            return render(request, 'home.html', {
                'error':
                    'Not enough questions available for the selected '
                    'filters. Please select All Units or Balanced difficulty.'
            })

        # -----------------------------------------
        # RANDOMLY SELECT QUESTIONS
        # -----------------------------------------

        section_a = random.sample(
            section_a_pool,
            section_a_count
        )

        section_b = random.sample(
            section_b_pool,
            section_b_count
        )

        section_c = random.sample(
            section_c_pool,
            section_c_count
        )

        # -----------------------------------------
        # COMBINE QUESTIONS
        # -----------------------------------------

        selected_questions = section_a + section_b + section_c

        # -----------------------------------------
        # SEND DATA TO QUESTION PAPER
        # -----------------------------------------

        return render(request, 'question_paper.html', {
            'questions': selected_questions,
            'subject': subject,
            'branch': branch,
            'semester': semester,
            'academic_year': academic_year,
            'exam_type': exam_type,
            'units': units,
            'marks': total_marks,
            'difficulty': difficulty,
            'question_type': question_type,
        })

    return render(request, 'home.html')