from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.models import Course, LessonProgress


profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/dashboard')
@login_required
def dashboard():
    courses = Course.query.all()
    progress_map = []
    
    for course in courses:
        course_progress = {}
        for lesson in course.lessons:
            progress = LessonProgress.query.filter_by(
                user_id=current_user.id, lesson_id=lesson.id
            ).first()
            course_progress.append({
                'lesson': lesson,
                'completed': progress.completed if progress else False
            })
        progress_map[course] = course_progress
    
    return render_template('user/dashboard.html', progress_map=progress_map)
