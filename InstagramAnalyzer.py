import instaloader, os, shutil


def mostrar_opciones():

    """ Muestra el menú de opciones y retorna la opción elegida """

    return int(input("1 - Actualizar seguidos y seguidores.\n2 - Actualizar seguidos.\n3 - Actualizar seguidores.\n4 - Usuarios a los que sigue y no le siguen.\n5 - Comparar seguidores antiguos y nuevos.\n6 - Cantidad de seguidores y seguidos.\n7 - Salir.\n\n"))
    

def cargar_perfil(usuario, contrasenia):

    """ Retorna el perfil correspondiente a un usuario y una contraseña """

    try:
        
        print(f'Iniciando la sesión de "{usuario}"...')
        
        L = instaloader.Instaloader()
        L.login(usuario, contrasenia)
        
        print("Sesión iniciada.\n\n")
        
        return instaloader.Profile.from_username(L.context, usuario)
    
    except:
        
        print('No se pudo iniciar sesión, comprobar los datos del archivo "cuenta.txt"')
        exit()
        
    
def leer_usuarios(nombre_archivo):

    """ Retorna una lista con los usuarios del archivo """
    
    try:
        with open(nombre_archivo, encoding = "UTF-8") as f:
            lista_usuarios = [usuario.replace("\n", "") for usuario in f]
    except FileNotFoundError:
        print(f"No se encontró el archivo '{nombre_archivo}'")
        exit()
    
    return lista_usuarios
    
    
def actualizar_seguidos(perfil):

    """ Actualiza los usuarios seguidos """
    
    print("Actualizando los seguidos...")
    
    shutil.copy2("seguidos.txt", 'copia_seguidos' + os.sep + "copia" + str(len(os.listdir("copia_seguidos")) + 1) + ".txt")
        
    with open("seguidos.txt", "w", encoding = "UTF-8") as f:
        cantidad = 0
        for seguido in perfil.get_followees():
            f.write(seguido.username + "\n")
            cantidad += 1
                
    print(f"Cantidad de seguidos: {cantidad}.")
        
        
def actualizar_seguidores(perfil):

    """ Actualiza los seguidores del usuario """
    
    print("Actualizando los seguidores...")
    
    shutil.copy2("seguidores.txt", 'copia_seguidores' + os.sep + "copia" + str(len(os.listdir("copia_seguidores")) + 1) + ".txt")

    with open("seguidores.txt", "w", encoding = "UTF-8") as f:
        cantidad = 0
        for seguido in perfil.get_followers(): 
            f.write(seguido.username + "\n")
            cantidad += 1
            
    print(f"Cantidad de seguidores: {cantidad}.")
    
    
def actualizar_seguidos_y_seguidores(perfil):

    """ Actualiza los usuarios seguidos y seguidores del usuario """

    actualizar_seguidos(perfil)
    print("\n")
    actualizar_seguidores(perfil)
    
    
def chequeador(perfil):

    """ Muestra los usuarios seguidos que no siguen al usuario """

    actualizar_seguidores(perfil)
    seguidores = leer_usuarios("seguidores.txt")
    
    print("\n")
    
    actualizar_seguidos(perfil)
    seguidos = leer_usuarios("seguidos.txt")
    
    lista = []

    for i in seguidos:
        if not i in seguidores:
            lista += [i]
            
    print("\nResultado:", lista)
    
    
def comparar(perfil):

    """ Muestra los usuarios que dejaron de seguir al usuario """
    
    seguidores_antiguos = leer_usuarios("seguidores.txt")
    
    actualizar_seguidores(perfil)
    
    seguidores = leer_usuarios("seguidores.txt")
      
    print(set(seguidores_antiguos).difference(set(seguidores)))
    
    
def cantidades(perfil):

    """ Muestra la cantidad de seguidores y seguidos """

    seguidores = leer_usuarios("seguidores.txt")
      
    seguidos = leer_usuarios("seguidos.txt")
      
    print(f"Cantidad de seguidores: {len(seguidores)}\nCantidad de seguidos: {len(seguidos)}.")
 

def crear_archivo(nombre):

    """ Crea un archivo """

    with open(nombre, "w"):
        pass
 
    
def preparar_archivos():

    """ Crea las carpetas y archivos que utiliza el programa """

    if not os.path.isdir("copia_seguidores"):
        os.mkdir("copia_seguidores")
        
    if not os.path.isdir("copia_seguidos"):
        os.mkdir("copia_seguidos")
        
    if not os.path.isfile("seguidores.txt"):
        crear_archivo("seguidores.txt")
    
    if not os.path.isfile("seguidos.txt"):
        crear_archivo("seguidos.txt")
        
    if not os.path.isfile("cuenta.txt"):
        print('Ingrese su usuario y contraseña:\n')
        with open("cuenta.txt", "w") as f:
            f.write(input("Usuario: ") + "\n")
            f.write(input("Contraseña: ") + "\n")
        print("\n")
        
        
def iniciar_sesion():

    """ Inicia la sesión del usuario """

    usuario, contrasenia = leer_usuarios("cuenta.txt")
    
    return cargar_perfil(usuario, contrasenia)
    
    
def main():

    print("\n\n~ Diseñado por Valentín Giorgetti | GitHub: github.com/ValentinGiorgetti ~\n\n")

    preparar_archivos()
    
    perfil = iniciar_sesion()

    opcion = mostrar_opciones()
    
    opciones = {1 : actualizar_seguidos_y_seguidores, 2 : actualizar_seguidos, 3 : actualizar_seguidores, 4 : chequeador, 5 : comparar, 6 : cantidades}

    while opcion in opciones:
        print("\n")
        opciones[opcion](perfil)
        print("\n")
        opcion = mostrar_opciones()
    
    
if __name__ == "__main__":
    main()