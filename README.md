# Patrimonio Vivo

Catálogo web de lugares patrimoniales de Chile, desarrollado con Python y Django para el Certamen N°2 de EIN082B.

Autor: **Bruno Rivas**

## Requisitos

Python 3.10 o superior.

## Instalación

Abre una terminal dentro de la carpeta del proyecto, donde está `manage.py`.

**1. Crear y activar el entorno virtual**

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS o Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

**2. Instalar las dependencias**

```bash
pip install -r requirements.txt
```

**3. Configurar la base de datos**

El proyecto usa SQLite, que no requiere instalar nada más. Estos comandos crean las tablas y cargan las categorías y lugares de ejemplo:

```bash
python manage.py migrate
python manage.py loaddata datos
```

**4. Crear el administrador**

```bash
python manage.py createsuperuser
```

**5. Ejecutar la aplicación**

```bash
python manage.py runserver
```

Abre <http://127.0.0.1:8000/>. El panel de administración está en <http://127.0.0.1:8000/admin/>.

## Usuarios y permisos

Entra a `/admin/` con el administrador y crea:

1. Un grupo `Editores` con los permisos para agregar y modificar `lugar patrimonial`.
2. Un usuario `editor` que pertenezca al grupo `Editores`.
3. Un usuario `consultor` sin grupo ni permisos.

## Pruebas

```bash
python manage.py test
```

## Requisitos funcionales

| Código | Dónde está |
|---|---|
| RF01 | Vista `inicio` y `inicio.html` |
| RF02 | Vista `catalogo` y `catalogo.html` |
| RF03 | Vista `detalle` y `detalle.html` |
| RF04 | Modelo `Categoria`, relacionado con `LugarPatrimonial` por `ForeignKey` |
| RF05 | Vista `por_categoria` |
| RF06 | `catalogo/admin.py` |
| RF07 | Menú en `base.html`, herencia de templates y archivos en `catalogo/static/` |
| RF08 | `LoginView` y `login.html` |
| RF09 | `LogoutView` y botón en `base.html` |
| RF10 | `@login_required` en las vistas de gestión |
| RF11 | `@permission_required` en `agregar` y `editar` |
| RF12 | Los decoradores protegen las vistas aunque se escriba la URL directamente |

## Imágenes

Las imágenes se guardan como URL. La fotografía del Museo a Cielo Abierto proviene de [Meteored](https://www.meteored.cl/noticias/ocio/la-galeria-mas-grande-de-santiago-esta-al-aire-libre-asi-puedes-recorrer-sus-murales-mas-espectaculares.html).
