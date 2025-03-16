# Generated by Django 5.1.7 on 2025-03-16 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_tasktable_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktable',
            name='priority',
            field=models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('URGENT', 'Urgent')], default='LOW', max_length=15),
        ),
        migrations.AlterField(
            model_name='tasktable',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed'), ('ARCHIVED', 'Archived')], default='IN_PROGRESS', max_length=15),
        ),
    ]
