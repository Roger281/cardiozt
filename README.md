# cardio_zt
## Requisitos
- Python3.5.5 - Python3.5.9
## Instalación
```bash
sudo apt install python3-pip # instalar gestor de paquetes si no existe
pip3 install virtualenv --user # instalar virtualenv para crear un entorno virtual de la app
mkdir ~/virtaulEnv # crear carpeta para almacenar el entorno virtual
python3 -m virtualenv ~/virtualEnv/cardioEnv # crear un entorno virtual
source ~/virtualEnv/cardioEnv/bin/activate # activar el entorno virtual
#Entrar en la carpeta del proyecto
pip install -r requirements.txt # instalar requeriemientos de la app
```

## Iniciar App
Para iniciar el serivcio se tienen que entrar a la carpeta `proyectoCardio` y ejecutar:
```bash
python manage.py runserver
```
### Entrar en admin
Agregar "/admin" a la url (Ejemplo: 127.0.0.1/admin).
usuario:admin
Contraseña:Pass1234
