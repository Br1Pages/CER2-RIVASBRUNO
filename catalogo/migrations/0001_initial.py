import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Categoria",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=80)),
                ("descripcion", models.TextField(verbose_name="descripción")),
            ],
        ),
        migrations.CreateModel(
            name="LugarPatrimonial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=120)),
                ("descripcion", models.TextField(verbose_name="descripción")),
                ("ubicacion", models.CharField(max_length=150, verbose_name="ubicación")),
                ("anio_construccion", models.IntegerField(verbose_name="año de construcción")),
                ("imagen", models.URLField(blank=True, verbose_name="URL de la imagen")),
                ("categoria", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="catalogo.categoria")),
            ],
            options={
                "verbose_name_plural": "lugares patrimoniales",
            },
        ),
    ]
