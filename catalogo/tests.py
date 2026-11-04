from django.contrib.auth.models import Permission, User
from django.core.management import call_command
from django.test import TestCase

from .models import Categoria, LugarPatrimonial


class PruebasDelSitio(TestCase):
    def setUp(self):
        self.murales = Categoria.objects.create(nombre="Murales", descripcion="Arte en muros")
        self.monumentos = Categoria.objects.create(nombre="Monumentos", descripcion="Obras")
        self.mural = LugarPatrimonial.objects.create(
            nombre="Mural de prueba", descripcion="Texto del mural", ubicacion="San Miguel",
            anio_construccion=2009, categoria=self.murales,
        )
        LugarPatrimonial.objects.create(
            nombre="Monumento de prueba", descripcion="Texto", ubicacion="Valdivia",
            anio_construccion=1671, categoria=self.monumentos,
        )
        self.consultor = User.objects.create_user("consultor", password="clave-de-prueba")
        self.editor = User.objects.create_user("editor", password="clave-de-prueba")
        self.editor.user_permissions.add(
            Permission.objects.get(codename="add_lugarpatrimonial"),
            Permission.objects.get(codename="change_lugarpatrimonial"),
        )
        self.datos = {
            "nombre": "Lugar nuevo", "descripcion": "Texto", "ubicacion": "Valparaíso",
            "anio_construccion": 1900, "imagen": "", "categoria": self.murales.id,
        }

    def test_inicio_presenta_la_fundacion(self):
        self.assertContains(self.client.get("/"), "Fundación Patrimonio Vivo")

    def test_catalogo_muestra_los_lugares(self):
        respuesta = self.client.get("/catalogo/")
        self.assertContains(respuesta, "Mural de prueba")
        self.assertContains(respuesta, "Monumento de prueba")

    def test_detalle_muestra_la_informacion(self):
        respuesta = self.client.get(f"/lugar/{self.mural.id}/")
        for texto in ["Mural de prueba", "Texto del mural", "San Miguel", "2009", "Murales"]:
            self.assertContains(respuesta, texto)

    def test_filtro_muestra_solo_una_categoria(self):
        respuesta = self.client.get(f"/categoria/{self.murales.id}/")
        self.assertContains(respuesta, "Mural de prueba")
        self.assertNotContains(respuesta, "Monumento de prueba")

    def test_iniciar_y_cerrar_sesion(self):
        respuesta = self.client.post("/login/", {"username": "editor", "password": "clave-de-prueba"})
        self.assertRedirects(respuesta, "/gestion/")
        self.assertRedirects(self.client.post("/logout/"), "/")
        self.assertRedirects(self.client.get("/gestion/"), "/login/?next=/gestion/")

    def test_menu_cambia_si_hay_sesion(self):
        self.assertContains(self.client.get("/"), "Iniciar sesión")
        self.client.force_login(self.consultor)
        self.assertContains(self.client.get("/"), "Cerrar sesión")

    def test_anonimo_va_al_login(self):
        for url in ["/gestion/", "/gestion/agregar/", f"/gestion/editar/{self.mural.id}/"]:
            self.assertRedirects(self.client.get(url), f"/login/?next={url}")

    def test_sin_permisos_no_ve_botones(self):
        self.client.force_login(self.consultor)
        respuesta = self.client.get("/gestion/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertNotContains(respuesta, "/gestion/agregar/")

    def test_sin_permisos_recibe_403_por_url_directa(self):
        self.client.force_login(self.consultor)
        self.assertEqual(self.client.get("/gestion/agregar/").status_code, 403)
        self.assertEqual(self.client.get(f"/gestion/editar/{self.mural.id}/").status_code, 403)

    def test_post_sin_permisos_no_guarda_cambios(self):
        self.client.force_login(self.consultor)
        self.assertEqual(self.client.post("/gestion/agregar/", self.datos).status_code, 403)
        self.assertFalse(LugarPatrimonial.objects.filter(nombre="Lugar nuevo").exists())

    def test_con_permiso_agrega_lugar(self):
        self.client.force_login(self.editor)
        self.assertRedirects(self.client.post("/gestion/agregar/", self.datos), "/gestion/")
        self.assertTrue(LugarPatrimonial.objects.filter(nombre="Lugar nuevo").exists())

    def test_con_permiso_modifica_lugar(self):
        self.client.force_login(self.editor)
        url = f"/gestion/editar/{self.mural.id}/"
        self.assertRedirects(self.client.post(url, self.datos), "/gestion/")
        self.mural.refresh_from_db()
        self.assertEqual(self.mural.nombre, "Lugar nuevo")

    def test_datos_de_ejemplo_se_cargan(self):
        call_command("loaddata", "datos", verbosity=0)
        self.assertGreaterEqual(LugarPatrimonial.objects.count(), 8)

    def test_no_faltan_migraciones(self):
        call_command("makemigrations", "--check", "--dry-run", verbosity=0)
