import instaloader, os, shutil, PySimpleGUI as sg
from webbrowser import open as abrir_web
from os.path import join, isdir, isfile
from threading import Thread


parametros_ventana = {"element_justification" : "center", 
                      "auto_size_text" : True, 
                      "auto_size_buttons" : True, 
                      "finalize" : True, 
                      "use_default_focus" : False,
                      "text_justification" : "center",
                      "icon" : join("componentes", "imagenes", "icono.ico")}

parametros_popup = {"title" : " Atención", 
                    "non_blocking" : True, 
                    "custom_text" : (" Aceptar ", None),
                    "icon" : join("componentes", "imagenes", "notification.ico")}

cartel = {"title" : " Atención", 
          "non_blocking" : False, 
          "custom_text" : (" Aceptar ", None),
          "icon" : join("componentes", "imagenes", "warning.ico")}
                    
parametros_texto = {"size": (30, 1), "font": ("None", 11)}

gif = join("componentes", "imagenes", "loading.gif")

transparente = join("componentes", "imagenes", "transparente.png")

perfil = None
finalizo = False
error = ""
cantidad = 0


def finalizar():

    """ Usado para la comunicación entre funciones de diferentes hilos """

    global finalizo
    finalizo = True
    

def cargar_perfil(usuario, contrasenia):

    """ Retorna el perfil correspondiente a un usuario y una contraseña """

    global perfil, error

    try:
        
        L = instaloader.Instaloader()
        L.login(usuario, contrasenia)
        
        perfil = instaloader.Profile.from_username(L.context, usuario)

        finalizar()
    
    except:

        error = 'Ocurrió un error al tratar de iniciar sesión.\n\nRevisar el archivo "componentes\cuenta.txt".\n'
        
    
def leer_usuarios(nombre_archivo):

    """ Retorna una lista con los usuarios del archivo """
    
    try:
        with open(nombre_archivo, encoding = "UTF-8") as f:
            lista_usuarios = [usuario.replace("\n", "") for usuario in f]
    except FileNotFoundError:
        sg.Popup(f'No se encontró el archivo "{nombre_archivo}"\n', **cartel)
        exit()
    
    return lista_usuarios
    

def actualizar_gif(window):

    """ Actualiza el gif de espera de la ventana """

    global finalizo, error

    while not finalizo:
        window["gif"].UpdateAnimation(gif, time_between_frames = 100)
        window.Refresh()
        if error:
            sg.Popup(error, **cartel)
            exit()
    window["gif"].Update(transparente)
    window["texto"].Update(visible = False)
    
    finalizo = False

    
def actualizar_seguidos(window, mostrar_mensaje = True):

    """ Actualiza los usuarios seguidos """

    def helper():
    
        global cantidad, error

        try:

            shutil.copy2(join("componentes", "seguidos.txt"), join("componentes", "copia_seguidos", "copia" + str(len(os.listdir(join("componentes", "copia_seguidos"))) + 1) + ".txt"))
            
            seguidos = [seguido.username for seguido in perfil.get_followees()]

            cantidad = len(seguidos)

            with open(join("componentes", "seguidos.txt"), "w", encoding = "UTF-8") as f:
                f.write('\n'.join(seguidos))
        
        except:

            error = "Ocurrió un error al actualizar los seguidos\n"

        finalizar()

    if mostrar_mensaje:
        window["texto"].Update("Actualizando los seguidos...", visible = True)
        
    Thread(target = helper).start()
    
    actualizar_gif(window)
    
    if mostrar_mensaje:    
        sg.Popup(f"Cantidad de seguidos: {cantidad}ㅤㅤㅤ\n", **parametros_popup)
        
        
def actualizar_seguidores(window, mostrar_mensaje = True):

    """ Actualiza los usuarios seguidores """

    def helper():
    
        global cantidad, error

        try:

            shutil.copy2(join("componentes", "seguidores.txt"), join("componentes", "copia_seguidores", "copia" + str(len(os.listdir(join("componentes", "copia_seguidores"))) + 1) + ".txt"))
            
            seguidores = [seguidor.username for seguidor in perfil.get_followers()]

            cantidad = len(seguidores)

            with open(join("componentes", "seguidores.txt"), "w", encoding = "UTF-8") as f:
                f.write('\n'.join(seguidores))

        except:

            error = "Ocurrió un error al actualizar los seguidores\n"
         
        finalizar()

    if mostrar_mensaje:
        window["texto"].Update("Actualizando los seguidores...", visible = True)
        
    Thread(target = helper).start()
    
    actualizar_gif(window)
    
    if mostrar_mensaje:    
        sg.Popup(f"Cantidad de seguidores: {cantidad}ㅤㅤㅤ\n", **parametros_popup)
    
    
def actualizar_seguidos_y_seguidores(window, mostrar_mensaje = False):

    """ Actualiza los usuarios seguidos y seguidores del usuario """
    
    if mostrar_mensaje:
        window["texto"].Update("Actualizando los seguidos y seguidores...", visible = True)
        actualizar_seguidos(window, False)
        
        window["texto"].Update("Actualizando los seguidos y seguidores...", visible = True)
        actualizar_seguidores(window, False)
    else:
        actualizar_seguidos(window)
        actualizar_seguidores(window)
    

def mostrar_multiline(texto, lista):

    """ Muestra una ventana con la información recibida por parámetros """

    layout = [[sg.Text(size = (35, 1))],
              [sg.Text(texto, **parametros_texto)],
              [sg.Text()],
              [sg.Multiline(lista, size = (32, 15), disabled = True)],
              [sg.Text()],
              [sg.Button(" Aceptar ")],
              [sg.Text()]]
              
    window = sg.Window("Resultado", layout, **parametros_ventana)
    
    window.Read()

    window.Close()

    
def not_followed_back(window):

    """ Muestra los usuarios seguidos que no siguen al usuario """
    
    actualizar_seguidos_y_seguidores(window, True)
    seguidores = leer_usuarios(join("componentes", "seguidores.txt"))
    seguidos = leer_usuarios(join("componentes", "seguidos.txt"))

    lista = ""

    for seguido in seguidos:
        if not seguido in seguidores:
            lista += seguido + "\n"

    if not lista:
        sg.Popup("No se encontraron seguidores que no hayan followback\n", **parametros_popup)
        return
    
    window.Hide()

    mostrar_multiline("Usuarios que no hicieron follow back", lista)
    
    window.UnHide()
    
    
def unfollowers(window):

    """ Muestra los usuarios que dejaron de seguir al usuario """
    
    seguidores_antiguos = leer_usuarios(join("componentes", "seguidores.txt"))
    
    window["texto"].Update("Actualizando los seguidores...", visible = True)
    actualizar_seguidores(window, False)
    seguidores = leer_usuarios(join("componentes", "seguidores.txt"))
      
    lista = "\n".join(set(seguidores_antiguos).difference(set(seguidores)))

    if not lista:
        sg.Popup("No se encontraron seguidores que hayan hecho unfollow\n", **parametros_popup)
        return

    window.Hide()
    
    mostrar_multiline("Usuarios que han hecho unfollow", lista)
    
    window.UnHide()
    

def crear_archivo(nombre):

    """ Crea un archivo """

    if os.path.isfile(nombre):
        return

    with open(nombre, "w"):
        pass
 

def preparar_archivos():

    """ Crea algunas carpetas y archivos que utiliza el programa """

    if isfile(join("componentes", "cuenta.txt")):
        return False
    
    if not isdir(join("componentes", "copia_seguidores")):
        os.makedirs(join("componentes", "copia_seguidores"))
    if not isdir((join("componentes", "copia_seguidos"))):
        os.makedirs(join("componentes", "copia_seguidos"))
        
    crear_archivo(join("componentes", "seguidores.txt"))
    crear_archivo(join("componentes", "seguidos.txt"))

    return True

    
def iniciar_programa():

    """ Solicita el usuario y contraseña para iniciar sesión """

    if not preparar_archivos():
        return
    
    columna_izquierda = [[sg.Text("Ingrese su usuario de Instagram")],
                         [sg.Text("Ingrese su contraseña de Instagram")]]                
    columna_izquierda = sg.Column(columna_izquierda, justification = "left")
    
    columna_derecha = [[sg.Input(key = "usuario", size = (20, 1))],
                       [sg.Input(key = "contraseña", size = (20, 1), password_char = "●")]]                
    columna_derecha = sg.Column(columna_derecha, justification = "left")
    
    layout = [[sg.Text(size = (45, 1))],
              [sg.Image(join("componentes", "imagenes", "logo.png"))],
              [sg.Text()],
              [columna_izquierda, columna_derecha],
              [sg.Text()],
              [sg.Button(" Aceptar ", key = "aceptar", size = (9, 1)), sg.Button("Salir", key = "salir", size = (9, 1))],
              [sg.Text()]]

    window = sg.Window(" InstagramAnalyzer", layout, **parametros_ventana)
    
    while True:
        event, values = window.Read()
        if event in (None, "salir"):
            window.Close()
            exit()
        if event == "aceptar":
            usuario = values["usuario"]
            contrasenia = values["contraseña"]
            if "" in (usuario, contrasenia):
                sg.Popup("Debe completar ambos campos\n", **parametros_popup)
            else:
                with open(join("componentes", "cuenta.txt"), "w") as f:
                    f.write(usuario + "\n")
                    f.write(contrasenia)
                break
                
    window.Close()
        
        
def iniciar_sesion():

    """ Inicia la sesión del usuario """
    
    try:
        usuario, contrasenia = leer_usuarios(join("componentes", "cuenta.txt"))
    except:
        sg.Popup('Ocurrió un error al tratar de iniciar sesión.\n\nRevisar el archivo "componentes\cuenta.txt"\n', **cartel)
        exit()
    
    layout = [[sg.Text(size = (45, 1))],
              [sg.Image(join("componentes", "imagenes", "logo.png"))],
              [sg.Text()],
              [sg.Text(f'Iniciando sesión de "@{usuario}"...', key = "texto"), sg.Image(gif, key = "gif")],
              [sg.Text()]]

    window = sg.Window(" InstagramAnalyzer | Iniciando sesión", layout, **parametros_ventana)
    
    Thread(target = cargar_perfil, args = (usuario, contrasenia)).start()
    
    actualizar_gif(window)
        
    window.Close()
        
    return usuario
        

def crear_ventana_menu(usuario):

    """ Crea la ventana del menú """
    
    layout = [[sg.Text(size = (50, 1))],
              [sg.Image(join("componentes", "imagenes", "logo.png"))],
              [sg.Text()],
              [sg.Text(f'@{usuario}', background_color = "#355070", **parametros_texto)],
              [sg.Text()],
              [sg.Button("Usuarios que no hicieron follow back", key = "not_followed_back", **parametros_texto)],
              [sg.Button("Actualizar seguidos y seguidores", key = "actualizar_ambos", **parametros_texto)],
              [sg.Button("Usuarios que hicieron unfollow", key = "unfollowers", **parametros_texto)],
              [sg.Button("Actualizar seguidores", key = "actualizar_seguidores", **parametros_texto)],
              [sg.Button("Actualizar seguidos", key = "actualizar_seguidos", **parametros_texto)],
              [sg.Button("GitHub", key = "github", **parametros_texto)],
              [sg.Button("Salir", key = "salir", **parametros_texto)],
              [sg.Text()],
              [sg.Column([[sg.Column([[sg.Text("                                                                ", key = "texto", visible = False)]], element_justification = "center"), sg.Column([[sg.Image(transparente, key = "gif")]], element_justification = "center")]], justification = "center")]]
    
    window = sg.Window(f' InstagramAnalyzer | @{usuario}', layout, **parametros_ventana)

    return window
        
        
def main():

    iniciar_programa()
    
    usuario = iniciar_sesion()

    ventana = crear_ventana_menu(usuario)
    
    opciones = {"actualizar_ambos" : actualizar_seguidos_y_seguidores, 
                "actualizar_seguidos" : actualizar_seguidos, 
                "actualizar_seguidores" : actualizar_seguidores, 
                "not_followed_back" : not_followed_back, 
                "unfollowers" : unfollowers,
                "github" : lambda foo : abrir_web("https://github.com/ValentinGiorgetti")}
                
    while True:
        event, value = ventana.Read()        
        if event in (None, "salir"):
            break
        opciones[event](ventana)
        
    
if __name__ == "__main__":
    main()
