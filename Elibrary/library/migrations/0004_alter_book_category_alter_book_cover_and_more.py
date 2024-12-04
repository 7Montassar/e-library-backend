# Generated by Django 5.1.3 on 2024-12-01 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_book_cover_book_books_title_7a737c_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('fiction', 'Fiction'), ('self_help', 'Self Help'), ('history', 'History'), ('crime', 'Crime'), ('thriller', 'Thriller'), ('horror', 'Horror'), ('science', 'Science'), ('biography', 'Biography'), ('business', 'Business'), ('philosophy', 'Philosophy'), ('politics', 'Politics'), ('classics', 'Classics'), ('computers', 'Computers')], default='fiction', max_length=20),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
