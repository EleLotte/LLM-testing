
import os
os.system("pip install openai==0.27.0")
os.system('cls')
import openai

#Intento de apertura para el documento de texto que contiene la API_KEY de OPENAI
#Si no encuentra el documento, pasa a solicitarla y preguntar si desea guardarla
#try:
#    file = open("api_key.txt", "r")
#    api_key=file.readline()
#    print(len(api_key))
#    file.close()
#except FileNotFoundError:
#seccion donde se solicita y guarda la API_KEY en un archivo llamado api_key.txt
key=input("Ingrese su API_KEY de OPENAI\n>> ")
api_key = key #@param {type:"string"}
os.environ["OPENAI_API_KEY"] = key    
archivo=input("Desea guardar la su API_KEY en un archivo por si la pierde? (y/n)\n>> ")
if archivo=="y" or archivo=="Y":
    local_file=open("api_key.txt", "wt")
    local_file.write(api_key)
   
#Las funciones asignan variables de entorno temporales que necesitan los
#comandos CLI de OPENAI

#Funcion para abrir el archivo preparado para el entrenamiento del modelo
def entrenarmodelodesdearchivo():
    nombre=input("Asegurese de guardar el archivo de entrenamiento en la misma carpeta que este programa"+
                 "\ningrese el nombre del archivo preparado para entrenamiento con todo y su extension\n>> ")
    file_path = nombre #@param {type:"string"}
    os.environ["FILE_PATH"] = file_path
    #retorna el nombre como ruta del archivo, el archivo deberia estar guardado
    #junto a este archivo para que funcione
    return nombre

#Funcion para abrir el archivo que se desea preparar para entrenar el modelo
def preparararchivo():
    nombre=input("Asegurese de guardar el archivo a entrenar en la misma carpeta que este programa"+
                 "Ingrese el nombre del archivo csv para preparar el entrenamiento\n"+
                 "(sin extension, solo el nombre)\n>> ")
    file_path = nombre #@param {type:"string"}
    os.environ["FILE_PATH"] = file_path+".csv"

    #Este es un comando de CLI de OPENAI que prepara el archivo para entrenamiento
    #hay que aceptar todo a excepcion de subdividir el archivo entre "training" y "validation"
    #posterior a eso, solo hay que aceptar convertir el archivo a JSON pues es lo que comsume
    #la API de OPENAI para el entrenamiento
    os.system("openai tools fine_tunes.prepare_data -f "+file_path+".csv")

    #retorna el nombre como ruta del archivo, el archivo deberia estar guardado
    #junto a este archivo para que funcione
    return nombre

#funcion de entrenamiento, solicita el nombre del modelo y un modelo base para entrenar    
def modeloynombre(filepath):
    #Solicitud del nombre que se le quiere poner al modelo
    model_sufix = input("Como se va a llamar el modelo al finalizar? \n>> ") #@param {type:"string"}
    #Seleccion del modelo de lenguaje para entrenar, desde el menos costoso al mas costoso
    #https://openai.com/pricing
    opcion=input("Elija el modelo a entrenar: (Ordenado del menos cosotoso al mas costoso)\n1.- Ada\n2.- Babbage\n3.- Curie\n4.- Davinci\n >> ")
    if opcion=="1":
        selection="ada"
    elif opcion=="2":
        selection="babbage"
    elif opcion=="3":
        selection="curie"
    elif opcion=="4":
        selection="davinci"
    else:
        exit()
    #selection = selection #@param {type:"string"}
    os.system("openai api fine_tunes.create -t "+filepath+" -m "+selection+" --suffix $model_sufix")

#Funcion para el seguimiento del modelo, asi se logra verificar el estado actual del entrenamiento del modelo,
#desde que es creado hasta que es entrenado y puesto en linea
def seguirmodelo():
    #Solicita ID del modelo, el cual se otorga cuando se manda a entrenar el modelo
    model_id = input("ingrese el id de su modelo entrenado\n>> ") #@param {type:"string"}
    #Comando de CLI de OPENAI para el seguimiento del estatus del modelo
    os.system("openai api fine_tunes.follow -i "+model_id)

#Cancela el entrenamiento del modelo, para ello se necesita su id y que no haya comenzando su entrenamiento, osea
#aun se encuentre en la fila
def cancelarafinamiento():
    idcancel=input("Ingrese el id del entrenamiento que desea cancelar\n>> ")
    #Comando de CLI de OPENAI para cancelar entrenamiento
    os.system("openai api fine_tunes.cancel -i "+idcancel)

#con esta funcion se hace una solicitud HTTP para obtener el documento de lista para los modelos entrenados con OPENAI
def capturarmodelos():
    import requests

    headers = {
        'Authorization': 'Bearer '+api_key,
    }

    response = requests.get('https://api.openai.com/v1/fine-tunes', headers=headers)
    print(response.content)
    #Guarda la informacion obtenida en un archivo JSON, alli se encuentra el ID del modelo que sirve para cancelarlo o
    #seguir el proceso de entrenamiento en caso de perder el ID
    local_file = 'modelos_propios.json'
    with open(local_file, 'wb')as file:
        file.write(response.content)
    
menu=""
#Menu con 7 opciones
#1.- crea a partir de un CSV un archivo listo para entrenar un modelo
#2.- sigue el proceso de entrenamiento de un modelo a partir de su id
#3.- inicia el proceso de entrenamiento desde la creacion del archivo de entrenamiento
#4.- inicia el proceso de entrenamiento desde un archivo de entrenamiento ya creado con anterioridad
#5.- cancela el entrenamiento de un modelo a partir de su ID y solo si aun se encuentra en lista de espera
#6.- Descarga la informacion sobre todos los modelos pertenecientes a la cuenta
#7.- cierra la app
while(menu!="7"):    
    menu=input("\n\n\nQue operacion desea realizar? seleccione una opcion:\n"+
          "1.- Crear archivo de entrenamiento\n"+
          "2.- Seguir el proceso de entrenamiento de un modelo\n"+
          "3.- Iniciar proceso desde 0\n"+
          "4.- Iniciar proceso a partir de un archivo de entrenamiento\n"+
          "5.- Cancelar entrenamiento\n"+
          "6.- Descargar informacion sobre modelos\n"+
          "7.- Salir\n>> ")


    if menu=="1":
        preparararchivo()
    elif menu=="2":
        seguirmodelo()
    elif menu=="3":
        ruta=preparararchivo()
        modeloynombre(ruta+"_prepared.jsonl")
    elif menu=="4":
        modeloynombre(entrenarmodelodesdearchivo())
    elif menu=="5":
        cancelarafinamiento()
    elif menu=="6":
        capturarmodelos()


