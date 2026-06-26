"""
Quiz Academy — Views
All admin and student views. Organized by role.
"""
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q

from quiz.models import (
    CustomUser, Quiz, Question, Subject,
    Option, QuizAttempt, StudentAnswer, Certificate
)
from quiz.forms import QuizForm, QuestionForm, OptionForm, StudentProfileForm


# ============================================================
# SHARED / HOME
# ============================================================

def home_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'admin':
            return redirect('index1')
        return redirect('stu_index')
    return redirect('student_login_view')


# ============================================================
# ADMIN AUTH
# ============================================================

def LoginUserView(request):
    msg = ''
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.user_type == 'admin':
            auth_login(request, user)
            return redirect('index1')
        msg = "Invalid email or password."
    return render(request, 'sign.html', {'msg': msg})


def logout_admin(request):
    auth_logout(request)
    return redirect('sign1')


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@login_required(login_url='sign1')
def index(request):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    students = CustomUser.objects.filter(user_type='student').annotate(
        score_sum=Sum('attempts__score'),
        quiz_count=Count('attempts')
    )
    total_students = students.count()
    total_quizzes = Quiz.objects.count()
    total_questions = Question.objects.count()
    total_attempts = QuizAttempt.objects.filter(is_completed=True).count()

    # Average score across all completed attempts
    avg_pct = 0
    completed = QuizAttempt.objects.filter(is_completed=True).select_related('quiz')
    if completed.exists():
        pct_sum = 0
        pct_count = 0
        for att in completed:
            tm = att.total_marks
            if tm > 0:
                pct_sum += (att.score / tm) * 100
                pct_count += 1
        avg_pct = round(pct_sum / pct_count, 1) if pct_count else 0

    context = {
        'n': request.user,
        'c': total_students,
        'q': total_questions,
        'total_quizzes': total_quizzes,
        'total_attempts': total_attempts,
        'avg_pct': avg_pct,
        'data': students,
    }
    return render(request, 'index.html', context)


# ============================================================
# ADMIN ANALYTICS
# ============================================================

@login_required(login_url='sign1')
def admin_analytics(request):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    # Core counts
    total_students = CustomUser.objects.filter(user_type='student').count()
    total_quizzes = Quiz.objects.count()
    active_quizzes = Quiz.objects.filter(is_active=True).count()
    total_attempts = QuizAttempt.objects.filter(is_completed=True).count()

    # Average score percentage
    avg_pct = 0
    completed = QuizAttempt.objects.filter(is_completed=True).select_related('quiz')
    pct_values = []
    for att in completed:
        tm = att.total_marks
        if tm > 0:
            pct_values.append((att.score / tm) * 100)
    if pct_values:
        avg_pct = round(sum(pct_values) / len(pct_values), 1)

    # Top 5 performers (by avg percentage across attempts)
    students = CustomUser.objects.filter(user_type='student').annotate(
        quiz_count=Count('attempts'),
        score_sum=Sum('attempts__score')
    ).filter(quiz_count__gt=0)

    top_performers = []
    for s in students:
        top_performers.append({
            'student': s,
            'avg_pct': s.average_score_percent,
            'quiz_count': s.quiz_count,
        })
    top_performers = sorted(top_performers, key=lambda x: x['avg_pct'], reverse=True)[:5]

    # Hardest questions (lowest correct_rate among those with ≥2 answers)
    hardest_questions = []
    for q in Question.objects.all():
        total_ans = StudentAnswer.objects.filter(question=q).count()
        if total_ans >= 1:
            correct_ans = StudentAnswer.objects.filter(question=q, is_correct=True).count()
            rate = round((correct_ans / total_ans) * 100, 1)
            hardest_questions.append({'question': q, 'rate': rate, 'total': total_ans})
    hardest_questions = sorted(hardest_questions, key=lambda x: x['rate'])[:5]

    # Subject-wise quiz count
    subjects = Subject.objects.annotate(quiz_count=Count('quizzes'))

    # Per-quiz avg score
    quiz_stats = []
    for quiz in Quiz.objects.all():
        attempts = QuizAttempt.objects.filter(quiz=quiz, is_completed=True)
        attempt_count = attempts.count()
        if attempt_count > 0:
            avg = round(sum((a.score / a.total_marks * 100) for a in attempts if a.total_marks > 0) / attempt_count, 1)
        else:
            avg = 0
        quiz_stats.append({'quiz': quiz, 'attempts': attempt_count, 'avg_pct': avg})

    context = {
        'total_students': total_students,
        'total_quizzes': total_quizzes,
        'active_quizzes': active_quizzes,
        'total_attempts': total_attempts,
        'avg_pct': avg_pct,
        'top_performers': top_performers,
        'hardest_questions': hardest_questions,
        'subjects': subjects,
        'quiz_stats': quiz_stats,
    }
    return render(request, 'admin_analytics.html', context)


# ============================================================
# ADMIN STUDENT VIEWS
# ============================================================

@login_required(login_url='sign1')
def add_student(request):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    msg = ''
    msg_type = 'danger'
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        enrollment_no = request.POST.get('enrollment', '').strip()
        attendance = request.POST.get('attendence', 0)
        cgpa = request.POST.get('cgpa', 0.0)
        review = request.POST.get('review', 0)
        branch = request.POST.get('branch', '').strip()
        proctor = request.POST.get('proctor', '').strip()

        if not all([name, email, password, enrollment_no]):
            msg = "All required fields must be filled."
        elif CustomUser.objects.filter(email=email).exists():
            msg = "This email is already registered."
        elif CustomUser.objects.filter(enrollment_no=enrollment_no).exists():
            msg = "This enrollment number is already registered."
        else:
            try:
                CustomUser.objects.create_user(
                    username=enrollment_no,
                    email=email,
                    password=password,
                    user_type='student',
                    enrollment_no=enrollment_no,
                    first_name=name,
                    attendance=int(attendance),
                    cgpa=float(cgpa),
                    review=int(review),
                    branch=branch,
                    proctor=proctor,
                )
                msg = f"Student '{name}' registered successfully!"
                msg_type = 'success'
            except Exception as e:
                msg = f"Error creating student: {str(e)}"

    return render(request, 'Add_student.html', {'s': msg, 'msg_type': msg_type})


@login_required(login_url='sign1')
def admin_student_detail(request, student_id):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    student = get_object_or_404(CustomUser, id=student_id, user_type='student')
    attempts = QuizAttempt.objects.filter(
        student=student, is_completed=True
    ).select_related('quiz').order_by('-start_time')

    attempt_data = []
    for att in attempts:
        attempt_data.append({
            'attempt': att,
            'percentage': att.percentage,
            'grade': att.grade,
            'total_marks': att.total_marks,
        })

    context = {
        'student': student,
        'attempt_data': attempt_data,
        'total_attempts': len(attempt_data),
        'avg_pct': student.average_score_percent,
    }
    return render(request, 'admin_student_detail.html', context)

@login_required(login_url='sign1')
def bulk_import_students(request):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    if request.method == 'POST' and request.FILES.get('csv_file'):
        import csv
        import io

        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return render(request, 'Add_student.html', {'s': 'Please upload a valid CSV file.', 'msg_type': 'danger'})

        decoded = csv_file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded))

        success_count = 0
        errors = []

        for i, row in enumerate(reader, start=2):
            try:
                name = row.get('name', '').strip()
                email = row.get('email', '').strip()
                password = row.get('password', '').strip()
                enrollment_no = row.get('enrollment_no', '').strip()
                branch = row.get('branch', '').strip()
                proctor = row.get('proctor', '').strip()
                attendance = int(row.get('attendance', 0) or 0)
                cgpa = float(row.get('cgpa', 0.0) or 0.0)

                if not all([name, email, password, enrollment_no]):
                    errors.append(f"Row {i}: Missing required fields.")
                    continue
                if CustomUser.objects.filter(email=email).exists():
                    errors.append(f"Row {i}: Email '{email}' already exists.")
                    continue
                if CustomUser.objects.filter(enrollment_no=enrollment_no).exists():
                    errors.append(f"Row {i}: Enrollment '{enrollment_no}' already exists.")
                    continue

                CustomUser.objects.create_user(
                    username=enrollment_no,
                    email=email,
                    password=password,
                    user_type='student',
                    first_name=name,
                    enrollment_no=enrollment_no,
                    branch=branch,
                    proctor=proctor,
                    attendance=attendance,
                    cgpa=cgpa,
                )
                success_count += 1
            except Exception as e:
                errors.append(f"Row {i}: {str(e)}")

        msg = f"{success_count} student(s) imported successfully."
        if errors:
            msg += f" {len(errors)} error(s): " + " | ".join(errors[:3])
        msg_type = 'success' if success_count > 0 else 'danger'
        return render(request, 'Add_student.html', {'s': msg, 'msg_type': msg_type})

    # Download blank CSV template
    if request.method == 'GET' and request.GET.get('download_template'):
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="student_import_template.csv"'
        writer = csv.writer(response)
        writer.writerow(['name', 'email', 'password', 'enrollment_no', 'branch', 'proctor', 'attendance', 'cgpa'])
        writer.writerow(['John Doe', 'john@example.com', 'password123', 'EN21CS001', 'Computer Science', 'Prof. Sharma', '90', '8.5'])
        return response

    return redirect('addstudent')

@login_required(login_url='sign1')
def student_report(request):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    students = CustomUser.objects.filter(user_type='student').annotate(
        quiz_count=Count('attempts'),
        total_score_agg=Sum('attempts__score')
    )
    student_data = []
    for s in students:
        student_data.append({
            'student': s,
            'quiz_count': s.quiz_count,
            'total_score': s.total_score_agg or 0,
            'avg_pct': s.average_score_percent,
        })

    return render(request, 'studentreport.html', {'student_data': student_data})


@login_required(login_url='sign1')
def download_report(request, student_id):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    from io import BytesIO
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.enums import TA_CENTER

    student = get_object_or_404(CustomUser, id=student_id, user_type='student')
    attempts = QuizAttempt.objects.filter(
        student=student, is_completed=True
    ).select_related('quiz').order_by('-start_time')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    title_style = ParagraphStyle('title', fontSize=20, alignment=TA_CENTER, textColor=colors.HexColor('#2563EB'), spaceAfter=6, fontName='Helvetica-Bold')
    elements.append(Paragraph("Quizopedia", title_style))

    sub_title_style = ParagraphStyle('subtitle', fontSize=11, alignment=TA_CENTER, textColor=colors.grey, spaceAfter=16)
    elements.append(Paragraph("Student Performance Report", sub_title_style))

    student_name = f"{student.first_name} {student.last_name}".strip() or student.username
    info_data = [
        ["Student Name", student_name, "Enrollment No", student.enrollment_no or "—"],
        ["Branch", student.branch or "—", "CGPA", str(student.cgpa)],
        ["Attendance", f"{student.attendance}%", "Total Quizzes", str(attempts.count())],
    ]
    info_table = Table(info_data, colWidths=[4*cm, 6*cm, 4*cm, 3*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#EFF6FF')),
        ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#EFF6FF')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1E40AF')),
        ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#1E40AF')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BFDBFE')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F8FAFF')]),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.5*cm))

    section_style = ParagraphStyle('section', fontSize=12, textColor=colors.HexColor('#1E40AF'), fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=6)
    elements.append(Paragraph("Quiz Attempt History", section_style))

    headers = ['#', 'Quiz Title', 'Score', 'Total', '%', 'Grade', 'Date', 'Tab Switches']
    table_data = [headers]
    for i, attempt in enumerate(attempts, 1):
        table_data.append([
            str(i),
            attempt.quiz.title,
            str(attempt.score),
            str(attempt.total_marks),
            f"{attempt.percentage}%",
            attempt.grade,
            attempt.start_time.strftime('%d %b %Y'),
            str(attempt.tab_switches),
        ])

    col_widths = [1*cm, 5.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.5*cm, 2.5*cm, 2*cm]
    attempts_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    attempts_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F7FF')]),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#BFDBFE')),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(attempts_table)
    elements.append(Spacer(1, 0.5*cm))

    avg = student.average_score_percent
    summary_style = ParagraphStyle('summary', fontSize=9, textColor=colors.grey, alignment=TA_CENTER)
    elements.append(Paragraph(f"Average Score: {avg}%  |  Generated by Quizopedia", summary_style))

    doc.build(elements)
    buffer.seek(0)

    filename = f"{student_name}_report.pdf"
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
# ============================================================
# ADMIN QUIZ MANAGEMENT
# ============================================================

@login_required(login_url='sign1')
def create_quiz(request):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewquiz')
    else:
        form = QuizForm()

    return render(request, 'createtest.html', {'form': form})


@login_required(login_url='sign1')
def view_quizzes(request):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    quizzes = Quiz.objects.select_related('subject').annotate(
        attempt_count=Count('attempts')
    ).order_by('-created_at')

    return render(request, 'view_quiz.html', {'quizzes': quizzes})


@login_required(login_url='sign1')
def edit_quiz(request, quiz_id):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('viewquiz')
    else:
        form = QuizForm(instance=quiz)

    return render(request, 'createtest.html', {'form': form, 'edit_mode': True, 'quiz': quiz})


@login_required(login_url='sign1')
def delete_quiz(request, quiz_id):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        quiz.delete()
    return redirect('viewquiz')


@login_required(login_url='sign1')
def toggle_quiz(request, quiz_id):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.is_active = not quiz.is_active
    quiz.save()
    return redirect('viewquiz')


# ============================================================
# ADMIN QUESTION MANAGEMENT
# ============================================================

@login_required(login_url='sign1')
def add_question(request):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('viewquestion')
    else:
        form = QuestionForm()

    # ← BUG FIX: missing return statement was here
    return render(request, 'questionadd.html', {'form': form})


@login_required(login_url='sign1')
def add_option(request, question_id):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question = question
            option.save()
            return redirect('viewquestion')
    else:
        form = OptionForm()

    return render(request, 'add_option.html', {'form': form, 'question': question})


@login_required(login_url='sign1')
def view_questions(request):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    quiz_filter = request.GET.get('quiz', '')
    questions = Question.objects.select_related('quiz').prefetch_related('options')

    if quiz_filter:
        questions = questions.filter(quiz_id=quiz_filter)

    quizzes = Quiz.objects.all()
    return render(request, 'showquestion.html', {
        'al': questions,
        'quizzes': quizzes,
        'selected_quiz': quiz_filter,
    })


@login_required(login_url='sign1')
def delete_question(request, question_id):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.delete()
    return redirect('viewquestion')


# ============================================================
# ADMIN ATTENDANCE & LEADERBOARD
# ============================================================

@login_required(login_url='sign1')
def view_attendance(request):
    if request.user.user_type != 'admin':
        return redirect('sign1')

    students = CustomUser.objects.filter(user_type='student').annotate(
        quiz_count=Count('attempts', filter=Q(attempts__is_completed=True))
    ).order_by('-quiz_count')

    return render(request, 'admin_attendance.html', {'students': students})


@login_required
def global_leaderboard(request):
    top_attempts = QuizAttempt.objects.filter(
        is_completed=True
    ).select_related('student', 'quiz').order_by('-score', 'tab_switches')[:20]

    template_name = 'leaderboard.html' if request.user.user_type == 'admin' else 'stu_leaderboard.html'
    return render(request, template_name, {'attempts': top_attempts})


# ============================================================
# STUDENT AUTH
# ============================================================

def student_login_view(request):
    msg = ''
    if request.method == 'POST':
        enroll_no = request.POST.get('enroll_no', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, enrollment_no=enroll_no, password=password)
        if user is not None and user.user_type == 'student':
            auth_login(request, user)
            return redirect('stu_index')
        msg = "Invalid Enrollment Number or Password."
    return render(request, 'stu_login.html', {'msg': msg})


def student_logout_view(request):
    auth_logout(request)
    return redirect('student_login_view')


# ============================================================
# STUDENT DASHBOARD & PROFILE
# ============================================================

@login_required(login_url='student_login_view')
def student_dashboard(request):
    if request.user.user_type != 'student':
        return redirect('student_login_view')

    # Filter: only active quizzes
    quizzes = Quiz.objects.filter(is_active=True).select_related('subject').order_by('-created_at')

    # Subject filter
    subject_filter = request.GET.get('subject', '')
    if subject_filter:
        quizzes = quizzes.filter(subject_id=subject_filter)

    subjects = Subject.objects.all()
    attempts = QuizAttempt.objects.filter(student=request.user, is_completed=True).select_related('quiz')
    attempted_quiz_ids = {att.quiz_id for att in attempts}

    context = {
        'quizzes': quizzes,
        'attempts': attempts,
        'attempted_quiz_ids': attempted_quiz_ids,
        'subjects': subjects,
        'selected_subject': subject_filter,
        'total_quizzes': quizzes.count(),
        'completed_count': len(attempted_quiz_ids),
        'avg_pct': request.user.average_score_percent,
    }
    return render(request, 'stu_index.html', context)


@login_required(login_url='student_login_view')
def student_profile(request):
    if request.user.user_type != 'student':
        return redirect('student_login_view')

    msg = ''
    msg_type = 'success'
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            msg = "Profile updated successfully!"
        else:
            msg = "Please fix the errors below."
            msg_type = 'danger'
    else:
        form = StudentProfileForm(instance=request.user)

    attempts = QuizAttempt.objects.filter(
        student=request.user, is_completed=True
    ).select_related('quiz').order_by('-start_time')[:5]

    context = {
        'form': form,
        'msg': msg,
        'msg_type': msg_type,
        'recent_attempts': attempts,
        'avg_pct': request.user.average_score_percent,
        'quizzes_attempted': request.user.quizzes_attempted,
    }
    return render(request, 'stu_profile.html', context)


@login_required(login_url='student_login_view')
def quiz_history(request):
    if request.user.user_type != 'student':
        return redirect('student_login_view')

    attempts = QuizAttempt.objects.filter(
        student=request.user, is_completed=True
    ).select_related('quiz', 'quiz__subject').order_by('-start_time')

    attempt_data = []
    for att in attempts:
        attempt_data.append({
            'attempt': att,
            'percentage': att.percentage,
            'grade': att.grade,
            'total_marks': att.total_marks,
        })

    context = {
        'attempt_data': attempt_data,
        'total': len(attempt_data),
        'avg_pct': request.user.average_score_percent,
    }
    return render(request, 'quiz_history.html', context)


# ============================================================
# STUDENT QUIZ TAKING
# ============================================================

@login_required(login_url='student_login_view')
def take_quiz(request, quiz_id):
    if request.user.user_type != 'student':
        return redirect('student_login_view')

    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)

    # Block re-entry if already completed
    existing = QuizAttempt.objects.filter(student=request.user, quiz=quiz, is_completed=True).first()
    if existing:
        return redirect('quiz_result', quiz_id=quiz.id)

    questions = quiz.questions.prefetch_related('options').all()

    if request.method == 'POST':
        tab_switches = int(request.POST.get('tab_switches', 0))
        time_taken = int(request.POST.get('time_taken', 0))

        # Create attempt
        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=0,
            tab_switches=tab_switches,
            time_taken_seconds=time_taken,
            is_completed=True,
            end_time=timezone.now(),
        )

        # Calculate score and save answers
        score = 0
        answers = []
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                try:
                    selected_option = Option.objects.get(id=int(selected_option_id), question=question)
                    is_correct = selected_option.is_correct
                    if is_correct:
                        score += question.marks
                    answers.append(StudentAnswer(
                        attempt=attempt,
                        question=question,
                        selected_option=selected_option,
                        is_correct=is_correct,
                    ))
                except Option.DoesNotExist:
                    pass
            else:
                # Unanswered question — record as skipped
                answers.append(StudentAnswer(
                    attempt=attempt,
                    question=question,
                    selected_option=None,
                    is_correct=False,
                ))

        attempt.score = score
        attempt.save()

        if answers:
            StudentAnswer.objects.bulk_create(answers)

        # Auto-generate certificate if score ≥ 40%
        total_marks = quiz.total_marks
        if total_marks > 0 and (score / total_marks) >= 0.40:
            Certificate.objects.get_or_create(attempt=attempt)

        # Update attendance (count = quizzes completed)
        request.user.attendance = QuizAttempt.objects.filter(
            student=request.user, is_completed=True
        ).count()
        request.user.save(update_fields=['attendance'])

        return redirect('quiz_result', quiz_id=quiz.id)

    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'take_quiz.html', context)


@login_required(login_url='student_login_view')
def quiz_result(request, quiz_id):
    if request.user.user_type != 'student':
        return redirect('student_login_view')

    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = get_object_or_404(QuizAttempt, student=request.user, quiz=quiz, is_completed=True)

    # Answer review
    answers = attempt.answers.select_related('question', 'selected_option').prefetch_related('question__options')
    answer_review = []
    for ans in answers:
        correct_option = ans.question.options.filter(is_correct=True).first()
        answer_review.append({
            'question': ans.question,
            'selected': ans.selected_option,
            'correct_option': correct_option,
            'is_correct': ans.is_correct,
        })

    # Certificate
    certificate = getattr(attempt, 'certificate', None)

    context = {
        'quiz': quiz,
        'attempt': attempt,
        'total_marks': attempt.total_marks,
        'percentage': attempt.percentage,
        'grade': attempt.grade,
        'answer_review': answer_review,
        'certificate': certificate,
    }
    return render(request, 'quiz_result.html', context)


# ============================================================
# CERTIFICATE
# ============================================================

@login_required(login_url='student_login_view')
def generate_certificate(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)

    if attempt.percentage < 40:
        if request.user.user_type == 'student':
            return redirect('quiz_result', quiz_id=attempt.quiz.id)
        return redirect('stu_index')

    cert, _ = Certificate.objects.get_or_create(attempt=attempt)

    context = {
        'cert': cert,
        'attempt': attempt,
        'student': request.user,
    }
    return render(request, 'certificate.html', context)
