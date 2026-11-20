# Guía explicativa de ejecución del proyecto de dengue

Esta guía te lleva desde la preparación del entorno hasta la obtención y revisión de resultados. Primero ejecutarás un modelo SIR pequeño para comprobar el flujo; después correrás las 999 simulaciones de dengue y su comparación independiente en Python.

Los comandos principales están preparados para Linux y Bash, usando la ruta de este proyecto. Se incluye una alternativa de preparación con PowerShell para Windows. Ejecuta cada bloque en la terminal indicada y comprueba su resultado antes de avanzar.

## 1 Entender dónde se ejecuta cada cosa

Trabajarás en dos entornos:

| Entorno | Qué haces allí | Cómo reconocerlo |
| --- | --- | --- |
| Tu equipo, fuera del contenedor | Preparar archivos, construir la imagen e iniciar Docker | Puedes ver el `Dockerfile` del proyecto |
| El contenedor | Ejecutar `lhsrun`, PRCC y Python | `pwd` muestra `/work` o una subcarpeta |

La **imagen** `lhsprcc` contiene las herramientas instaladas. El **contenedor** es una ejecución de esa imagen. El **volumen** conecta la carpeta `work` de tu equipo con `/work` dentro del contenedor: ambos nombres apuntan a los mismos archivos.

```text
Tu equipo                          Contenedor
Proyecto/work/       ← volumen →   /work/
   ejecucion_01/                      ejecucion_01/
```

Guardar los resultados bajo `/work` permite conservarlos después de salir del contenedor.

## 2 Comprobar Docker

**En tu equipo**, abre una terminal y ejecuta:

```bash
docker --version
docker info
```

El primero comprueba que existe el comando. El segundo comprueba que puedes comunicarte con el motor de Docker. Debe terminar sin un error de conexión o permisos. Si Docker no está instalado, prepara primero Docker para tu sistema; si usas Docker Desktop, debe estar iniciado y configurado para contenedores Linux.

No necesitas instalar NumPy, SciPy, gcc ni gnuplot en el Python o sistema de tu equipo: el `Dockerfile` los instala dentro de la imagen. La construcción requiere acceso a los repositorios de paquetes que utiliza.

## 3 Preparar una ejecución nueva

### Linux con Bash

**En tu equipo**, entra en la raíz del proyecto:

```bash
cd ~/Downloads/dengue
ls Dockerfile scripts/lhsrun vendor/lhsprcc_minimum_tar.gz models/dengue.txt models/ejemplo_sir.txt scripts/analisis_prcc.py
```

Las comillas permiten usar una ruta con espacios y paréntesis. `ls` debe mostrar los seis archivos. No descomprimas ni cambies el nombre de `lhsprcc_minimum_tar.gz`: el Dockerfile espera ese nombre exacto.

Prepara una carpeta para esta corrida:

```bash
mkdir -p work
mkdir work/ejecucion_01
cp models/dengue.txt models/ejemplo_sir.txt scripts/analisis_prcc.py work/ejecucion_01/
```

La carpeta nueva evita sobrescribir los resultados existentes de `work/out_ejemplo_sir/`. Si `ejecucion_01` ya existe, detente y utiliza otro nombre, por ejemplo `ejecucion_02`, en todos los comandos posteriores. El segundo `mkdir` da un error precisamente para hacer visible esa situación.

Las copias son las entradas de esta ejecución. Si después modificas el modelo de la raíz, la copia ya preparada no se actualiza automáticamente.

### Alternativa para Windows con PowerShell

**En tu equipo**, abre PowerShell en la carpeta que contiene el Dockerfile. Usa tu ubicación real para entrar en ella. Después:

```powershell
Get-Item Dockerfile, scripts/lhsrun, vendor/lhsprcc_minimum_tar.gz, models/dengue.txt, models/ejemplo_sir.txt, scripts/analisis_prcc.py
New-Item -ItemType Directory -Path work -Force
New-Item -ItemType Directory -Path work/ejecucion_01 -ErrorAction Stop
Copy-Item models/dengue.txt, models/ejemplo_sir.txt, scripts/analisis_prcc.py -Destination work/ejecucion_01/
```

Ejecuta las instrucciones por bloques. Si la creación de `ejecucion_01` falla porque ya existe, usa otro nombre antes de copiar archivos. Los comandos dentro del contenedor serán los mismos que en Linux porque allí trabajarás con Bash.

## 4 Construir la imagen

**En tu equipo, desde la raíz del proyecto**, ejecuta:

```bash
docker build -t lhsprcc .
```

`-t lhsprcc` asigna un nombre a la imagen. El punto final indica que el directorio actual es el contexto de construcción, donde Docker debe encontrar el Dockerfile y los archivos que este copia.

Durante la construcción se instala el entorno, se incorpora el paquete del curso y se compila `prcc_fix`. Este ejecutable corrige el manejo de empates al calcular rangos; será el utilizado por defecto. También se comprueba que un modelo de ejemplo pueda traducirse a C.

Debes llegar al final sin errores. Esa prueba de construcción verifica la traducción del ejemplo, pero todavía no comprueba toda la simulación ni sus resultados.

Construye la imagen inicialmente y cuando cambies el Dockerfile, el script `lhsrun` incorporado o el paquete del curso. Editar únicamente un modelo dentro de `work` no exige reconstruirla.

## 5 Entrar en el contenedor

**En tu equipo, en la raíz del proyecto**, usa uno de estos comandos.

Linux con Bash:

```bash
docker run --rm -it -v "$PWD/work:/work" lhsprcc
```

Windows con PowerShell:

```powershell
docker run --rm -it -v "${PWD}/work:/work" lhsprcc
```

`--rm` elimina el contenedor al salir; los archivos del volumen permanecen. `-it` abre una terminal interactiva. `-v` conecta las carpetas. El comando abre Bash dentro de la imagen.

**A partir de aquí, dentro del contenedor**, ejecuta:

```bash
pwd
ls
cd /work/ejecucion_01
ls
command -v lhsrun teval1 prcc_fix gcc gnuplot ps2pdf
python3 -c 'import numpy, scipy, matplotlib; print("Bibliotecas científicas disponibles")'
```

El primer `pwd` debe mostrar `/work`. En `ejecucion_01` debes encontrar los dos modelos y el script de Python. `command -v` debe mostrar rutas para todas las herramientas y Python debe imprimir el mensaje indicado.

## 6 Probar primero con el modelo SIR

**Dentro del contenedor, en `/work/ejecucion_01`**:

```bash
lhsrun ejemplo_sir.txt
```

Este modelo usa 100 combinaciones de parámetros y simula 100 días. Sirve para comprobar el circuito técnico antes del experimento de dengue.

El script muestra cuatro etapas:

| Etapa | Qué sucede | Qué archivo permite comprobarla |
| --- | --- | --- |
| 1 Traducción | `teval1` convierte el modelo a C | `temp1.c` |
| 2 Compilación | gcc construye el simulador | `run1` y `compile.log` |
| 3 Simulación | Se resuelven las ecuaciones para las muestras LHS | Trayectorias `0001` a `0100`, y archivos `lhs*` |
| 4 PRCC | Se calculan asociaciones parciales por rangos | `prcc.log` y `prcc.0001` a `prcc.0003` |

Al final se convierten gráficos PostScript a PDF cuando la herramienta está disponible.

Revisa:

```bash
cat out_ejemplo_sir/compile.log
cat out_ejemplo_sir/prcc.log
head -n 1 out_ejemplo_sir/lhsmatrix
head -n 3 out_ejemplo_sir/0001
ls out_ejemplo_sir/*.pdf
```

El registro de compilación puede estar vacío si no hubo advertencias. El registro PRCC debe informar finalización. La cabecera de `lhsmatrix` del SIR actual es `3 100 3 101`: tres parámetros, 100 muestras, tres salidas y 101 tiempos almacenados. Las columnas de cada trayectoria son tiempo, S, I y R.

En este ejemplo, `N0` está muestreado, pero no interviene en las ecuaciones ni en las condiciones iniciales. Úsalo como prueba técnica y recuerda ese detalle al interpretar su PRCC.

## 7 Ejecutar el modelo de dengue

**Dentro del contenedor, desde `/work/ejecucion_01`**:

```bash
lhsrun dengue.txt
```

El comando crea `out_dengue/`. Ejecuta 999 combinaciones de nueve parámetros, con semilla `20261118`, durante 365 días. El integrador RK4 avanza con paso de 0.05 días y guarda resultados cada 5 días.

Espera a que vuelva el indicador de la terminal. La duración depende del equipo; la ausencia temporal de mensajes no permite decidir por sí sola que el proceso se ha detenido.

Comprueba la salida:

```bash
cat out_dengue/compile.log
cat out_dengue/prcc.log
head -n 1 out_dengue/lhsmatrix
head -n 3 out_dengue/0001
tail -n 1 out_dengue/0001
ls out_dengue/prcc.000*
ls out_dengue/*.pdf
```

La cabecera esperada es `9 999 4 74`. Cada trayectoria debe tener 74 filas y cinco columnas: tiempo, `ih`, `ivr`, `ch`, `R0`. La primera fila corresponde al día 0 y la última al día 365. Los cuatro archivos PRCC siguen ese mismo orden de salidas.

El mensaje final «Listo» no garantiza por sí solo una corrida completa. El script puede ocultar un fallo del simulador en una tubería o continuar tras un fallo de PRCC. Revisa los registros y los datos antes de interpretar las figuras.

## 8 Ejecutar la comparación independiente

**Dentro del contenedor, desde `/work/ejecucion_01`**:

```bash
python3 analisis_prcc.py out_dengue figuras
```

El primer argumento indica dónde están los datos del software. El segundo indica dónde guardar las figuras y el CSV.

Python realiza cuatro tareas:

1. Lee la matriz LHS y las trayectorias originales.
2. Resuelve de nuevo las mismas 999 combinaciones con LSODA, un integrador diferente.
3. Calcula PRCC independientes y muestra diferencias frente al software.
4. Calcula el pico, su día y el acumulado al día 365; genera PNG y CSV.

El programa necesita toda la carpeta `out_dengue`, incluidas las trayectorias numeradas y `lhsmatrix`. Los archivos `prcc.000*` guardados en la raíz del repositorio no bastan para esta comparación.

En la terminal verás diferencias máximas de trayectorias y PRCC. El README del proyecto documenta un acuerdo de aproximadamente 0.001 o mejor para PRCC corregidos. Investiga discrepancias superiores y cualquier `NaN`; el script informa diferencias, pero no aplica un umbral automático de aprobación.

La comparación comprueba coherencia entre implementaciones. Para saber si el modelo representa una población real hacen falta datos y validación epidemiológica adicionales.

## 9 Comprobar y abrir los resultados

**Dentro del contenedor**:

```bash
ls figuras
cat figuras/prcc_outcomes_escalares.csv
```

Debes encontrar:

| Archivo | Qué explica |
| --- | --- |
| `fig1_trayectorias.png` | Mediana y bandas percentiles entre escenarios |
| `fig2_prcc_tiempo.png` | Cómo cambia el PRCC de cada parámetro con el tiempo |
| `fig3_prcc_outcomes.png` | PRCC del acumulado, pico y día del pico |
| `prcc_outcomes_escalares.csv` | Coeficientes, valores p y tamaños de muestra |

Sal del contenedor:

```bash
exit
```

**En tu equipo**, abre `work/ejecucion_01/figuras/` con el explorador de archivos. Los PDF del software estarán en `work/ejecucion_01/out_dengue/`, por ejemplo `prccvals.pdf`, `stats.pdf` y `signif.pdf` cuando se hayan generado correctamente.

En esta corrida, «tamaño final» significa acumulado al día 365. El día del pico se calcula en una cuadrícula diaria y solo para muestras con el R0 implementado mayor que uno. La [guía del proyecto](GUIA_PROYECTO.md) explica la revisión pendiente de esa fórmula bajo control vectorial y sus consecuencias para interpretar el filtro.

## 10 Repetir una corrida o cambiar el modelo

Crea otra carpeta, por ejemplo `work/ejecucion_02/`, copia allí las entradas y repite el flujo. Dentro del contenedor cambia a `/work/ejecucion_02` antes de ejecutar.

`lhsrun` reutiliza `out_<nombre_del_modelo>/` si ya existe. Cambiar parámetros y volver a ejecutarlo allí puede sobrescribir archivos y dejar otros antiguos; una carpeta nueva facilita saber qué resultados pertenecen a cada experimento.

Conserva juntos los modelos, la matriz LHS, las trayectorias, los registros y las figuras. Si modificas `dengue.txt`, comprueba qué debes sincronizar en Python:

| Cambio | Ajuste necesario |
| --- | --- |
| Ecuaciones | Actualizar también `rhs` y, cuando corresponda, `R0f` |
| Orden o número de parámetros LHS | Revisar `PARAMS`, etiquetas, lectura y argumentos del modelo |
| Condiciones iniciales | Actualizar `y0` |
| Horizonte de tiempo | Revisar el intervalo de integración y `tfine` |
| Orden de `$plot` | Revisar las columnas de las trayectorias y los archivos PRCC que lee Python |
| Frecuencia de almacenamiento | Revisar la correspondencia con la cuadrícula diaria usada para comparar |

El script de análisis está preparado para el dengue actual. No debe ejecutarse sobre `out_ejemplo_sir` como si fuera un analizador genérico.

### Cambiar la frecuencia del PRCC

Por ejemplo, dentro del contenedor y en una carpeta de ejecución nueva:

```bash
lhsrun dengue.txt 5
```

El número 5 pide calcular PRCC cada cinco filas de tiempo almacenadas. Con salidas cada cinco días, representa un espaciado aproximado de 25 días. No cambia el número de muestras ni el paso de integración. El valor predeterminado es 3; si PRCC falla, el script reintenta con 5, 10 y 20. Comprueba en la terminal cuál se utilizó realmente.

### Comparar con el ejecutable original

Para una comparación explícita en otra carpeta de ejecución puedes usar:

```bash
PRCC=prcc lhsrun dengue.txt
```

La asignación selecciona el programa original solo para ese comando. Sus resultados pueden verse afectados por el fallo de empates descrito en la guía general. No lo ejecutes sobre la carpeta que quieres conservar como resultado corregido.

La comparación automática de Python con ambas versiones requiere que los `prcc.000*` originales estén dentro de `out_dengue/prcc_original/`, correspondan a las mismas muestras y usen los mismos tiempos que los corregidos. Esa carpeta no se crea automáticamente al seleccionar `PRCC=prcc`.

## 11 Resolver problemas frecuentes

| Problema | Qué comprobar o hacer |
| --- | --- |
| `docker: command not found` | Docker debe estar instalado y disponible en la terminal del equipo |
| Error al conectar con el motor | Inicia el servicio o Docker Desktop y comprueba permisos con `docker info` |
| Docker no encuentra el Dockerfile | Ejecuta `docker build` desde la raíz que lo contiene |
| `/work` aparece vacío | Revisa que lanzaste `docker run` desde la raíz y montaste su carpeta `work` |
| `lhsrun: command not found` | Comprueba que estás dentro del contenedor construido con este Dockerfile |
| `Uso: lhsrun modelo.txt [N]` | Comprueba el directorio actual con `pwd` y la existencia del modelo con `ls` |
| Error de `teval1` | Revisa directivas, puntos y coma, nombres y condiciones iniciales del modelo |
| Error de compilación | Lee `out_dengue/compile.log`; se espera `$Rk4` para este flujo LHS |
| PRCC falla o reintenta | Lee `prcc.log`, verifica parámetros variables y observa si termina con un N mayor |
| Python no encuentra SciPy | Ejecuta el Python del contenedor, donde se instalaron las bibliotecas |
| Python no encuentra `lhsmatrix` | Confirma que `lhsrun` terminó y pasaste la carpeta completa correcta |
| Error de formas, columnas o tiempos en Python | Comprueba que las salidas corresponden al dengue actual y no a un modelo modificado |
| Faltan PDF | Revisa si existen `.ps` y si `command -v ps2pdf` encuentra el conversor |
| Permiso denegado al escribir | Comprueba permisos de la carpeta anfitriona montada en `/work` |

Si existen los PostScript pero faltan PDF, puedes convertir uno manualmente dentro del contenedor:

```bash
cd /work/ejecucion_01/out_dengue
ps2pdf prccvals.ps prccvals.pdf
cd /work/ejecucion_01
```

Así verás el error del conversor, que el flujo automático puede ocultar.

## 12 Criterios para dar la ejecución por terminada

- La construcción de la imagen termina sin errores.
- La prueba SIR produce trayectorias, registro PRCC y gráficos.
- La corrida dengue contiene 999 trayectorias coherentes con el horizonte y las columnas esperadas.
- Los registros de compilación y PRCC no muestran errores pendientes.
- Python completa la comparación con diferencias investigadas y sin fallos numéricos pendientes.
- La carpeta `figuras` contiene los tres PNG y el CSV, y puedes abrirlos desde tu equipo.
- Se conservan las entradas exactas junto con sus resultados.

Los comandos se han revisado contra el Dockerfile, `lhsrun`, los modelos y el script de análisis del repositorio. No se ejecutó una corrida completa para validar esta guía: Docker no está disponible en el entorno de revisión.
