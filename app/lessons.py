from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.models import Lesson, LessonProgress


lesson_bp = Blueprint('lessons', __name__)


@lesson_bp.route('/lesson/<int:lesson_id>')
@login_required
def lesson_detail(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    progress = LessonProgress.query.filter_by(
        user_id=current_user.id, lesson_id=lesson.id
    ).first()
    return render_template(
        'lessons/lesson_detail.html',
        lesson=lesson,
        progress=progress)


@lesson_bp.route('/lesson/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    progress = LessonProgress.query.filter_by(
        user_id=current_user.id, lesson_id=lesson.id
    ).first()
    if not progress:
        progress = LessonProgress(
            user_id=current_user.id,
            lesson_id=lesson.id,
            completed=True)
    else:
        progress.completed = True
    db.session.commit()
    flash('Урок отмечен как завершённый!')
    return redirect(url_for('lessons.lesson_detail', lesson_id=lesson.id))
