# Instalación de Tensorflow >2.10 para permitir uso de GPU en Windows 11
Tensorflow dejo de dar soporte a Windows nativo en la version 2.10 asi que es necesario el uso de una distribucion Linux o el uso de WSL2.
Es por eso que este Markdown sirve como guia para como hacerlo. Por si acaso toda la documentación oficial está en [Install TensorFlow with pip](https://www.tensorflow.org/install/pip#windows-wsl2_1)

## 1. Instalacion drivers NVIDIA
Hay que comprobar que nuestra grafica NVIDIA es compatible con Tensorflow y descargar sus drivers correspondientes. Comprobar la compatibilidad es simple, unicamente hay que ir a esta pagina [Nvidia GPU drivers](https://www.nvidia.com/en-us/drivers/) y buscar nuestra GPU. Si estamos usando un portatil hay que buscar las series que pone `notebooks` y ahi ya nos saldran las graficas de portatiles. Hacemos la busqueda y nos redigira a la pagina para descargar los drivers. Descargamos la mas reciente. 
> Si tenemos la aplicacion de Nvidia GeForce Experience o similar, ya existe un apartado para actualizar drivers y lo podemos hacer desde ahi.

## 2. Instalar CUDA y cuDNN
Instalaremos CUDA y cuDNN. Nos metemos a la pagina de descarga de [CUDA](https://developer.nvidia.com/cuda-toolkit-archive) y descargamos la ultima version estable. Hacemos lo mismo para [cuDNN](https://developer.nvidia.com/cudnn) y posiblemente nos pedira una cuenta de desarrollador. 

Instalaremos primero CUDA, que nos creara la carpeta con todo en
```
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\
```
Esta ruta sera la que aparezca mas tarde en `CUDA_PATH`

Ahora con el zip que habremos descargado de cuDNN lo extraemos dentro de esa carpeta de version de CUDA. Lo recomendable es cambiarle el nombre a la carpeta para que sea mas facil el siguiente paso. Deberiamos tener algo como esta ruta una vez extraido
```
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\cudnn-8.9.7.29
```

## 2.5 Añadir CUDA y cuDNN a variables del PATH
Tenemos que añadir al PATH las variables de entorno. Seguramente se nos abra creado la ruta de CUDA, guardada como `CUDA_PATH` o `CUDA_PATH_V11_8`. Tenemos que definir algunas en PATH
```PowerShell
%CUDA_PATH%\bin #es posible que esta ya este definida pero con la ruta absoluta
%CUDA_PATH%\libnvvp #igual que esta
%CUDA_PATH%\include
%CUDA_PATH%\cudnn-8.9.7.29\bin #por este motivo hemos cambiado el nombre del directorio cuDNN, pero es simplemente hacer referencia a la carpeta bin
```
> Al acabar de cambiar las rutas del PATH es posible y recomendable que reiniciemos el ordenador.

## 3. Comprobamos que todo esta bien
Vamos a comprobar que las instalaciones se han hecho correctamente. Abrimos una terminal cmd y escribimos 
```PowerShell
nvidia-smi
```
Nos deberia aparecer algo como `Driver Version: 561.09` y `CUDA Version: 12.6`. Deberia aparecer tambien nuestra grafica.

Ahora comprobamos cuDNN
```PowerShell
nvcc --version
```
Si no se reconoce el comando es que no se ha instalado cuDNN bien. Sino deberia aparecer en alguna linea algo como `Cuda compilation tools, release 12.0, V12.0.140`
> El paso de instalar en nuestra maquina cuDNN no tengo claro si es necesario porque mas tarde dentro de WSL hace falta volver a instalarlo, asi que simplemente hacemos las dos.

## 4. Instalacion WSL2
Necesitamos instalar WSL si no lo tenemos ya. Toda la informacion sobre WSL se puede encontrar en [Basic Commands for WSL](https://learn.microsoft.com/en-us/windows/wsl/basic-commands). Vamos a ver los pasos que considero necesarios unicamente.

Para ello ejecutamos una terminal de PowerShell con derechos de administrador y escribimos
```PowerShell
wsl --install
```
Una vez finalizado, comprobamos las distribuciones
```PowerShell
wsl -l -v
```
Podemos cambiar la distro que haya por defecto (marcado con un *) haciendo 
```PowerShell
wsl --set-default <distro_name>
```
Y por ultimo, comprobamos que podemos abrir wsl
```PowerShell
wsl #Para ejecutar la distro por defecto
wsl --distribution <distro_name> #Para ejecutar una distro especifica
```

## 5. Ejecucion de WSL
Primero de todo vamos a actualizar los paquetes mas recientes.
```bash
sudo apt update && sudo apt upgrade
```
Ejecutamos ahora el WSL donde haremos la instalacion. Lo primero es comprobar otra vez CUDA y cuDNN
```bash
nvidia-smi
nvcc --version
```
En caso de que nvcc no exista, ejecutamos lo siguiente
```bash
sudo apt install nvidia-cuda-toolkit
```
Una vez acabe volvemos a comprobar
```bash
nvcc --version
```

## 6. Abrir WSL en VSCode
Toda la documentacion para este paso esta en [Set up VSCode](https://learn.microsoft.com/en-us/windows/python/web-frameworks#set-up-visual-studio-code), pero voy a intentar resumirlo.

Vamos a abrir el WSL en VSCode para hacer uso de la instalacion. Para ello descargamos la extension de [WSL oficial de Microsoft](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl). Una vez instalada posiblemente haga falta reiniciar VSCode. 

Abrimos una nueva terminal WSL con nuestra distro correspondiente.
Una vez se conecte, necesitamos python, pip y venv. Al igual python ya esta instalado.
```bash
python3 --version
```
Si no lo esta lo primero es 
```bash
sudo apt update && sudo apt upgrade
```
y luego ya podemos hacer
```bash
sudo apt upgrade python3
sudo apt install python3-pip
sudo apt install python3-venv
```

Con eso hecho, creamos un nuevo entorno virtual que sera de Linux, a diferencia de uno que ya podamos tener creado y luego lo activamos
```bash
python3 -m venv .venvWSL
source .venv/bin/activate
```

Abrimos el proyecto como un servidor remoto que nos permite usar WSL como entorno de desarrollo. Para ello, en la carpeta del proyecto hacemos
```bash
code .
```
Y se nos abrira una nueva pestaña de VSCode conectada. Es posible que nos pida permiso para ejecutar la accion. Cuando acabe podremos ver en la esquina inferior izquierda un recuadro con una forma como de rayo y el nombre de nuestra distro

## 7. Volver a instalar la extension de Python y Jupyter en el WSL
Necesitamos volver a instalar las extensiones para que el WSL en VSCode sea capaz de ejecutar codigo.

## 8. Instalar paquetes necesarios para correr Tensorflow
Si estamos haciendo esta instalacion tenemos que descomentar `tensorflow[and-cuda]` del archivo `requirements.txt` y comentar `tensorflow`. Con eso hecho y el entorno virtual activado, ejecutamos
```bash
pip install -r requirements.txt
```
y nos deberia instalar las librerias necesarias para usar tensorflow con la GPU.

## 9. Compobar que esta reconociendo la GPU
En el notebook `7. tensorflow-introduccion` hay un apartado `Aceleración por GPU` donde podremos probar si funciona. En el output del primer bloque de codigo del apartado deberia salir algo como esto
```
Is there a GPU available: 
[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
Is the Tensor on GPU #0:  
True
```
Y con eso la instalación de Tensorflow para usar la GPU está finalizada.
