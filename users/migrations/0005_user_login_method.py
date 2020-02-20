# Generated by Django 3.0.3 on 2020-02-20 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200219_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_method',
            field=models.CharField(choices=[('email', 'Email'), ('github', 'Git hub'), ('kakao', 'Kakao')], default='email', max_length=50),
        ),
    ]
