from django.db import models


class Student(models.Model):

    name = models.TextField(verbose_name='Имя')
    birth_date = models.DateField(
        null=True,
        verbose_name='Дата рождения'
    )

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return self.name


class Course(models.Model):

    name = models.TextField(verbose_name='Наименование')
    students = models.ManyToManyField(
        Student,
        blank=True,
        verbose_name='Студенты на курсе'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name