from django.shortcuts import render
from django.db import Error
from appMovies.models import Genero, Peliculas
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from bson import ObjectId

# Create your views here.

def inicio(request):
    return render(request, "inicio.html")

# ////////////////////////////// Generos

def vistaAgregarGenero(request):
    return render(request, "agregarGenero.html")


@csrf_exempt
def agregarGenero(request):
    
    try:
        nombre=request.POST['newGenero']
        
        # se crea un objeto de tipo genero
        genero=Genero(genNombre=nombre)
        genero.save()
        mensaje='Genero agregado correctamente'
        
    except Error as error:
        mensaje=str(error)
    
    retorno={"mensaje":mensaje}
    
    return render(request, 'agregarGenero.html',retorno )


# ////////////////////////////////// Peliculas


def listarPeliculas(request):
    peliculas= Peliculas.objects.all()
    # peliculas= Peliculas.objects.all().values()
    retorno= {"peliculas": list(peliculas)}
    
    # return JsonResponse(retorno)
    return render(request, 'listarPeliculas.html',retorno )


# def consultarPeliculaById(request, id):
#     pelicula= Peliculas.objects.get(pk=ObjectId(id))
#     generos= Genero.objects.all()
    
#     retorno = {"peliculas": pelicula, "generos": generos}
#     return render(request, "", retorno)

def vistaAgregarPeliculas(request):
    generos= Genero.objects.all()
    retorno= {"generos": generos}
    return render(request, "agregarPeliculas.html", retorno)




def agregarPelicula(request):
    try:
        codigoCall = request.POST['codigo']
        tituloCall = request.POST['titulo']
        protagonistaCall = request.POST['protagonista']
        duracionCall = int(request.POST['duracion'])
        resumenCall = request.POST['resumen']
        fotoCall = request.FILES['foto']
        idGenero = int(request.POST['idGenero'])
        
        genero = Genero.objects.get(pk=idGenero)
        
        # crear objeto pelicula}
        
        pelicula=Peliculas(codigo=codigoCall,
                           titulo=tituloCall,
                           protagonista=protagonistaCall,
                           duracion=duracionCall,
                           resumen=resumenCall,
                           foto=fotoCall,
                           pelGenero=genero)
        
        pelicula.save()
        mensaje="Pelicula agregada correctamente"
        
        peliculas= Peliculas.objects.all()
 
    except Error as error:
        mensaje=str(error)
        
    retorno={"mensaje":mensaje,"peliculas": list(peliculas), "idPelicula":pelicula.id}
    return render(request, "listarPeliculas.html", retorno)














