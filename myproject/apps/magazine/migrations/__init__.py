from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modification Date and Time')),
                ('meta_keywords', models.CharField(blank=True, help_text='Separate keywords with commas.', max_length=255, verbose_name='Keywords')),
                ('meta_description', models.CharField(blank=True, max_length=255, verbose_name='Description')),
                ('meta_author', models.CharField(blank=True, max_length=255, verbose_name='Author')),
                ('meta_copyright', models.CharField(blank=True, max_length=255, verbose_name='Copyright')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authored_ideas2', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_ideas2', to='categories.Category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Idea',
                'verbose_name_plural': 'Ideas',
            },
        ),
        migrations.CreateModel(
            name='IdeaTranslations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=7, verbose_name='Language')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('idea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ideas2.Idea', verbose_name='Idea')),
            ],
            options={
                'verbose_name': 'Idea Translations',
                'verbose_name_plural': 'Idea Translations',
                'ordering': ['language'],
                'unique_together': {('idea', 'language')},
            },
        ),
        migrations.AddConstraint(
            model_name='idea',
            constraint=models.UniqueConstraint(condition=models.Q(_negated=True, author=None), fields=('title',), name='unique_titles_for_each_author2'),
        ),
        migrations.AddConstraint(
            model_name='idea',
            constraint=models.CheckConstraint(check=models.Q(title__iregex='^\\S.*\\S$'), name='title_has_no_leading_and_trailing_whitespaces2'),
        ),
    ]