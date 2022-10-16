# Generated by Django 4.1.1 on 2022-10-16 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('department_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.department')),
                ('instructor_name', models.CharField(max_length=120)),
                ('instructor_email', models.CharField(max_length=60)),
                ('semester_code', models.CharField(max_length=20)),
                ('course_num', models.CharField(max_length=20)),
                ('course_name', models.CharField(max_length=150)),
                ('section', models.CharField(max_length=5)),
                ('capacity', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=70)),
                ('meeting_days', models.CharField(max_length=20)),
                ('start_time', models.CharField(max_length=30)),
                ('end_time', models.CharField(max_length=30)),
            ],
            bases=('app.department',),
        ),
    ]
