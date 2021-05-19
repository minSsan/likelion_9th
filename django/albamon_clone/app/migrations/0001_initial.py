# Generated by Django 3.2 on 2021-05-18 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('job_area', models.CharField(max_length=200)),
                ('detail', models.TextField(blank=True)),
                ('location', models.CharField(max_length=200)),
                ('wage', models.IntegerField()),
                ('job', models.TextField()),
                ('applicant', models.IntegerField()),
            ],
        ),
    ]