from rest_framework import serializers, exceptions
from django_testing import settings
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, students_data):
        if len(students_data) > settings.MAX_STUDENTS_PER_COURSE:
            raise exceptions.ValidationError(
                f'Максимально допустимое число студентов на курсе превышено: {settings.MAX_STUDENTS_PER_COURSE}'
            )
        return students_data