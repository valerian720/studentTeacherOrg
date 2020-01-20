# Generated by Django 2.2.3 on 2019-11-03 20:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
            },
        ),
        migrations.CreateModel(
            name='Klass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Start', models.TimeField()),
                ('Finish', models.TimeField()),
            ],
            options={
                'verbose_name': 'Пара',
                'verbose_name_plural': 'Пары',
            },
        ),
        migrations.CreateModel(
            name='LesType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Description', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'Тип',
                'verbose_name_plural': 'Типы',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Semester', models.IntegerField()),
                ('Year', models.IntegerField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Group')),
            ],
            options={
                'verbose_name': 'План',
                'verbose_name_plural': 'Планы',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Photo', models.ImageField(blank=True, null=True, upload_to='uploadsTeachers/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Преподаватель',
                'verbose_name_plural': 'Преподаватели',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('StartDay', models.DateField()),
                ('FinishDay', models.DateField()),
                ('LessonType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.LesType')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Plan')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Teacher')),
            ],
            options={
                'verbose_name': 'Предмет',
                'verbose_name_plural': 'Предметы',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Photo', models.ImageField(blank=True, null=True, upload_to='uploadsStudents/')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Студент',
                'verbose_name_plural': 'Студенты',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Data', models.DateField()),
                ('Theme', models.CharField(max_length=300)),
                ('Description', models.TextField(null=True)),
                ('klass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Klass')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Subject')),
            ],
            options={
                'verbose_name': 'Занятие',
                'verbose_name_plural': 'Занятия',
            },
        ),
        migrations.CreateModel(
            name='HW',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Dls', models.FileField(upload_to='uploadsHW/')),
                ('Description', models.TextField(null=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Lesson')),
            ],
            options={
                'verbose_name': 'Домашняя работа',
                'verbose_name_plural': 'Домашние работы',
            },
        ),
        migrations.CreateModel(
            name='AddStuff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Dls', models.FileField(upload_to='uploadsAS/')),
                ('Description', models.TextField(null=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Lesson')),
            ],
            options={
                'verbose_name': 'Дополнительный материал',
                'verbose_name_plural': 'Дополнительные материалы',
            },
        ),
    ]
