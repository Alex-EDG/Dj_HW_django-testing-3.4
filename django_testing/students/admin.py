from django.contrib import admin
from students.models import Student, Course

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'birth_date')
    list_filter = ['name', 'birth_date']
    search_fields = ('name', 'birth_date',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')
    list_filter = ['name', 'students__name', 'students__birth_date']
    search_fields = ('name', 'students__name', 'students__birth_date')