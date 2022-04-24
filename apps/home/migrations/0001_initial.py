# Generated by Django 3.2.11 on 2022-04-23 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tovar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sklad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obiem', models.IntegerField(default=100, verbose_name='Обьем в литрах')),
                ('status', models.CharField(choices=[('Ожидается', 'Ожидается'), ('Принято', 'Принято'), ('В_пути', 'В_пути'), ('Доставлено', 'Доставлено')], max_length=128)),
                ('date', models.DateTimeField(auto_now=True)),
                ('accept', models.CharField(default='', max_length=128)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.company')),
                ('tovar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.tovar', verbose_name='Тип Товара')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
