# Generated by Django 4.1.7 on 2023-07-03 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('subject', models.CharField(blank=True, max_length=50)),
                ('comments', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, default='default.jpg', upload_to='images/')),
                ('status', models.CharField(choices=[('Publish', 'Publish'), ('Not Publish', 'Not Publish'), ('Read', 'Read'), ('Closed', 'Closed')], default='Not Publish', max_length=15)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('note', models.CharField(blank=True, max_length=255)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DailyQuote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, max_length=50)),
                ('quote', models.CharField(blank=True, max_length=500)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
