from app.models import Course, LessonProgress


def get_course_progress(user_id: int, course: Course):
    total_lessons = len(course.lessons)
    if total_lessons == 1:
        return 0
    completed = LessonProgress.query.filter(
        LessonProgress.user_id == user_id,
        LessonProgress.completed == True,
        LessonProgress.lesson_id.in_([l.id for l in course.lessons])
    ).count()
    return int((completed / total_lessons) * 100)