# InstagramAnalyzer  <img src="https://i.imgur.com/VhJ2Hcr.png" width="40" style="vertical-align:middle">

InstagramAnalyzer es una aplicación desarrollada en Python que permite: 

- Llevar un registro de los seguidores y seguidos de una cuenta de Instagram.

- Saber qué usuarios han dejado de seguir a la cuenta.

- Saber qué usuarios no han hecho un "follow back".


Para usar la aplicación se debe ejecutar "InstagramAnalyzer.exe", luego se debe ingresar el usuario y contraseña de la cuenta de Instagram que se quiere monitorear. Una vez hecho esto se mostrará un menú con las diferentes opciones.

Los datos de inicio de sesión (usuario y contraseña) únicamente se ingresan al iniciar la aplicación por primera vez, luego serán recordados para un uso posterior. Estos datos se almacenan en el archivo "cuenta.txt", donde la primer línea se corresponde con el nombre de usuario y la segunda línea se corresponde con la contraseña. Si se quiere utilizar la aplicación con otra cuenta, se pueden modificar los datos de ese archivo.

Cada vez que se actualicen los seguidores o seguidos de la cuenta se creará una copia del archivo anterior en la carpeta "copia_seguidores" o "copia_seguidos" respectivamente. Esos archivos consisten en una lista de los nombres de usuario de los seguidores y los seguidos por la cuenta.

~ Versión de Python utilizada: 3.6.8

~ Versión de instaloader utilizada: 4.5.4

#### Algunas imágenes

<p align="center">
  <img src="https://i.imgur.com/ihx4bps.png">
</p>
