from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LugarForm
from .models import Categoria, LugarPatrimonial


# ---------- Páginas públicas ----------

def inicio(request):
    return render(request, "inicio.html")


def catalogo(request):
    lugares = LugarPatrimonial.objects.all()
    categorias = Categoria.objects.all()
    return render(request, "catalogo.html", {"lugares": lugares, "categorias": categorias})


def por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    lugares = LugarPatrimonial.objects.filter(categoria=categoria)
    categorias = Categoria.objects.all()
    return render(
        request,
        "catalogo.html",
        {"lugares": lugares, "categorias": categorias, "categoria_elegida": categoria},
    )


def detalle(request, lugar_id):
    lugar = get_object_or_404(LugarPatrimonial, id=lugar_id)
    return render(request, "detalle.html", {"lugar": lugar})


# ---------- Área de gestión ----------

@login_required
def gestion(request):
    lugares = LugarPatrimonial.objects.all()
    return render(request, "gestion.html", {"lugares": lugares})


@login_required
@permission_required("catalogo.add_lugarpatrimonial", raise_exception=True)
def agregar(request):
    if request.method == "POST":
        form = LugarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("gestion")
    else:
        form = LugarForm()
    return render(request, "formulario.html", {"form": form})


@login_required
@permission_required("catalogo.change_lugarpatrimonial", raise_exception=True)
def editar(request, lugar_id):
    lugar = get_object_or_404(LugarPatrimonial, id=lugar_id)
    if request.method == "POST":
        form = LugarForm(request.POST, instance=lugar)
        if form.is_valid():
            form.save()
            return redirect("gestion")
    else:
        form = LugarForm(instance=lugar)
    return render(request, "formulario.html", {"form": form})
