from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    Name=models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    Photo=models.ImageField(upload_to='uploadsTeachers/',blank=True, null=True)
    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
    def __str__(self):
        return self.Name


#class Schedule(models.Model):
#    Name=models.CharField(max_length=200)
#    class Meta:
#        verbose_name = 'Расписание'
#        verbose_name_plural = 'Расписания'
#    def __str__(self):
#        return self.Name

class Klass(models.Model):#номер пары
    Name=models.CharField(max_length=200)
    Start=models.TimeField()
    Finish=models.TimeField()
    class Meta:
        verbose_name = 'Пара'
        verbose_name_plural = 'Пары'
    def __str__(self):
        return self.Name

class LesType(models.Model):
    Name=models.CharField(max_length=200)
    Description = models.TextField(null=True)
    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
    def __str__(self):
        return self.Name


class Group(models.Model):
    Name=models.CharField(max_length=200)
    #schedule=models.ForeignKey(Schedule, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
    def __str__(self):
        return self.Name

class Student(models.Model):
    Name=models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    Photo=models.ImageField(upload_to='uploadsStudents/',blank=True, null=True)
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
    def __str__(self):
        return self.Name
		
class Plan(models.Model):
    Name=models.CharField(max_length=200)
    Semester=models.IntegerField()
    Year=models.IntegerField()
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'План'
        verbose_name_plural = 'Планы'
    def __str__(self):
        return self.Name

class Subject(models.Model):#предмет
    Name=models.CharField(max_length=200)
    StartDay=models.DateField()
    FinishDay=models.DateField()
    LessonType=models.ForeignKey(LesType, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    plan=models.ForeignKey(Plan,on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
    def __str__(self):
        return self.Name

class Lesson(models.Model):#занятие
    Data=models.DateField()
    Theme=models.CharField(max_length=300)
    #schedule=models.ForeignKey(Schedule,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    klass=models.ForeignKey(Klass,on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
    Description=models.TextField(null=True)
    def __str__(self):
        return '{0} {1} {2} {3}'.format(self.Data, self.klass, self.subject, self.Theme)

class HW(models.Model):
    Name=models.CharField(max_length=200)
    lesson=models.ForeignKey(Lesson,on_delete=models.CASCADE)
    Dls=models.FileField(upload_to='uploadsHW/')
    Description=models.TextField(null=True)
    class Meta:
        verbose_name = 'Домашняя работа'
        verbose_name_plural = 'Домашние работы'
    def __str__(self):
        return self.Name

class AddStuff(models.Model):
    Name=models.CharField(max_length=200)
    lesson=models.ForeignKey(Lesson,on_delete=models.CASCADE)
    Dls=models.FileField(upload_to='uploadsAS/')
    Description=models.TextField(null=True)
    class Meta:
        verbose_name = 'Дополнительный материал'
        verbose_name_plural = 'Дополнительные материалы'
    def __str__(self):
        return self.Name