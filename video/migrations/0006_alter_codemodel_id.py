# Generated by Django 4.1 on 2022-09-02 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0005_delete_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codemodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
