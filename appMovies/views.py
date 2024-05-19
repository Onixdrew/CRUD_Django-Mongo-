from django.shortcuts import render,redirect
from django.db import Error
from appMovies.models import Genero, Peliculas
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from bson import ObjectId
import os
from django.utils.http import urlencode
from GestioPeliculas import settings
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
       
        if 'foto' in request.FILES:
            fotoCall = request.FILES['foto']
        
        idGenero = ObjectId(request.POST['idGenero'])
        
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
        
    retorno={"mensaje":mensaje,"peliculas": list(peliculas)}
    return redirect("/vistaListarPeliculas/")





def consultarPeliculaPorId(request,id):
    convObjecId=ObjectId(id)
    pelicula=Peliculas.objects.get(pk=convObjecId)
    generos= Genero.objects.all()
    selectGenero= Genero.objects.get(pk=ObjectId(pelicula.pelGenero_id))
    retorno={"pelicula":pelicula, "generos":generos, 'selectGenero':selectGenero}
    
    return render(request, "actualizarPelicula.html", retorno)



def actualizarPeliculas(request):
    try:
        
        # extraigo el id la pelicula que se va actualizar para usarlo como criterio
        peliculaUpdate= Peliculas.objects.get(pk= ObjectId(request.POST['idPeliculaUpdate']))
        
        peliculaUpdate.codigo = int(request.POST['codigo'])
        peliculaUpdate.titulo = request.POST['titulo']
        peliculaUpdate.protagonista = request.POST['protagonista']
        peliculaUpdate.duracion = int(request.POST['duracion'])
        peliculaUpdate.resumen = request.POST['resumen']
        idGenero = ObjectId(request.POST['idGenero'])
        
        genero = Genero.objects.get(pk=idGenero)
        peliculaUpdate.pelGenero=genero
        
        if 'foto' in request.FILES:
            foto = request.FILES.get('foto')
        
        if (foto):
            os.remove(os.path.join(settings.MEDIA_ROOT +'/'+ str(peliculaUpdate.foto)))
            
            peliculaUpdate.foto=foto
            
        peliculaUpdate.save()
        mensaje='Pelicula actualizada'
    
    except Error as error:
        mensaje= str(error)
        
    # messages.success(request, 'La película se actualizó correctamente.')
    retorno = urlencode({'mensaje': mensaje}) 
    # return JsonResponse(retorno)
    return redirect("/vistaListarPeliculas/")
        


def eliminarPelicula(request, id):
    
    try:
        
        eliminarMovie= Peliculas.objects.get(pk=ObjectId(id))
        eliminarMovie.delete()
        mensaje='Pelicula eliminada Correctamente'
    
    except Error as error:
        mensaje= str(error)
        
    retorno = urlencode({'mensaje': mensaje}) 
    # return JsonResponse(retorno)
    return redirect( "/vistaListarPeliculas/")








