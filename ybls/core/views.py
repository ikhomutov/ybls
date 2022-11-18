from django.shortcuts import render, get_object_or_404

from . import models


def levels_list_view(request):
    levels = models.Lesson.objects.order_by(
        'level'
    ).values_list(
        'level', flat=True
    ).distinct()
    context = {
        'levels': levels
    }
    return render(request, 'core/levels_list.html', context)


def subjects_list_view(request, level):
    subjects = models.Subject.objects.filter(
        lessons__level=level
    ).distinct()
    context = {
        'subjects': subjects,
        'level': level,
    }
    return render(request, 'core/subjects_list.html', context)


def subject_detail_view(request, level, subject_id):
    subject = get_object_or_404(models.Subject, pk=subject_id)
    lessons = subject.lessons.filter(level=level)
    context = {
        'level': level,
        'subject': subject,
        'lessons': lessons,
    }
    return render(request, 'core/subject_detail.html', context)


def lesson_detail_view(request, lesson_id):
    lesson_queryset = models.Lesson.objects.prefetch_related('contents__materials')
    lesson = get_object_or_404(lesson_queryset, pk=lesson_id)
    context = {
        'lesson': lesson,
    }
    return render(request, 'core/lesson_detail.html', context)