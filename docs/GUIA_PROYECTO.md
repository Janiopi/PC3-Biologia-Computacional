# Guía del proyecto de dengue y análisis de sensibilidad

Este proyecto estudia cómo cambia una epidemia simulada de dengue cuando se modifican parámetros de transmisión, recuperación y mortalidad de los mosquitos. Combina un modelo de ecuaciones diferenciales, muestreo de parámetros mediante hipercubo latino y análisis de sensibilidad mediante correlaciones parciales de rangos.

La pregunta central es: **dentro de los rangos propuestos, qué parámetros se asocian más con el tamaño, la intensidad y el momento de una epidemia simulada**. Los resultados describen el comportamiento del modelo; los archivos actuales no incluyen datos de vigilancia, ajuste a una localidad ni validación epidemiológica con observaciones.

## 1 Propósito y alcance

El trabajo tiene dos objetivos conectados:

1. Representar el ciclo de transmisión humano → mosquito → humano y un control que aumenta la mortalidad del vector.
2. Explorar la incertidumbre de los parámetros y ordenar su influencia sobre distintas salidas del modelo.

Una simulación responde qué ocurre con una combinación de parámetros. Las 999 simulaciones LHS muestran qué comportamientos aparecen al cubrir sus rangos. El PRCC resume asociaciones entre cada parámetro y una salida, ajustando por los demás parámetros.

El repositorio también contiene una verificación numérica: resuelve las mismas combinaciones con otro integrador y vuelve a calcular los PRCC en Python. Esa comparación puede detectar errores de implementación, pero no demuestra que las hipótesis biológicas representen una población real.

## 2 Mapa de archivos

| Archivo o carpeta | Función | Cuándo consultarlo |
| --- | --- | --- |
| `dengue.txt` | Modelo vigente, condiciones iniciales, rangos y configuración LHS | Para entender la ciencia que se simula |
| `ejemplo_sir.txt` | Modelo SIR pequeño con 100 muestras | Para practicar el flujo |
| `lhsrun` | Automatiza traducción, compilación, simulación, PRCC y conversión a PDF | Para entender la ejecución |
| `Dockerfile` | Instala herramientas y construye `prcc_fix` | Para reproducir el entorno |
| `lhsprcc_minimum_tar.gz` | Paquete del curso con ejecutables, fuentes y ejemplos | Para estudiar el motor original |
| `prcc_tieset.patch` | Registra la línea que corrige el manejo de empates | Para entender la diferencia entre ejecutables |
| `analisis_prcc.py` | Resuelve en SciPy, compara y genera figuras y CSV | Para entender la verificación y el análisis adicional |
| `README_DOCKER.md` | Instrucciones operativas, principalmente para Windows | Para instalar y ejecutar |
| `avance_laboratorio.txt` | Propuesta preliminar e ideas para el informe | Como antecedente; sus rangos y pendientes no representan todo el estado actual |
| `work/` | Entradas y salidas persistentes del contenedor | Para ejecutar sin perder resultados |
| `work/out_ejemplo_sir/` | Corrida SIR guardada con datos, C generado, registros y gráficos | Para inspeccionar una ejecución concreta |
| `fig1_trayectorias.png`, `fig2_prcc_tiempo.png`, `fig3_prcc_outcomes.png` | Figuras existentes de dengue | Para leer los resultados guardados |
| `prcc.0001` a `prcc.0004` en la raíz | PRCC temporales guardados para las cuatro salidas de dengue | Para consultar coeficientes y valores p |
| `mnt_user-data_outputs_resultados_prcc_prcc_original_prcc.000*` | Copias guardadas de resultados del ejecutable original | Para comparaciones históricas |
| `prcc_outcomes_escalares.csv` | PRCC de tamaño acumulado, pico, día del pico y R0 | Para interpretar los resultados resumidos |

Los resultados actuales están en `results/ejecucion_dengue/`; incluyen una carpeta completa `out_dengue/`. La corrida SIR está en `results/ejecucion_sir/`. Los PNG, CSV y PRCC históricos se conservan por separado en `results/historicos_dengue/`. `work/` se reserva para nuevas ejecuciones.

## 3 Conceptos biológicos del modelo

### Compartimentos humanos y del mosquito

Los humanos siguen un modelo SEIR:

```text
Susceptibles → Expuestos → Infecciosos → Recuperados
     sh           eh           ih            rh
```

Un expuesto está infectado y atraviesa la incubación; todavía no transmite en este modelo. Un humano infeccioso puede infectar mosquitos. Los recuperados no vuelven al compartimento susceptible.

Los mosquitos siguen un modelo SEI:

```text
Susceptibles → Expuestos → Infecciosos
    svr           evr           ivr
```

No hay recuperación del mosquito. La mortalidad actúa sobre sus tres compartimentos.

La transmisión cruza ambas poblaciones: `ivr` genera nuevas exposiciones humanas y `ih` genera nuevas exposiciones de mosquitos. No hay transmisión directa entre humanos en las ecuaciones.

### Fracciones y denominadores

Los humanos están expresados como fracciones de una población constante: `sh + eh + ih + rh = 1`. Por ejemplo, `ih = 0.001` representa 10 infecciosos si se interpreta una población de 10 000 personas. Esa población es una escala para interpretar resultados; no es un parámetro de `dengue.txt`.

Los mosquitos se expresan respecto de su población basal, equivalente a `m` mosquitos por humano. Así, para una población humana `Nh`, el número de mosquitos infecciosos sería `ivr × m × Nh`. `ivr` no es la proporción infecciosa entre los mosquitos actualmente vivos: esa proporción sería `ivr / (svr + evr + ivr)`.

`ch` acumula las nuevas entradas humanas al estado infeccioso. No pertenece a la suma de los cuatro compartimentos humanos. Como empieza en cero, excluye a los humanos que ya eran infecciosos al inicio.

### Tasas y tiempos medios

Una tasa tiene unidades de inverso de tiempo. Con tiempo en días, `gamma_h = 0.2` por día corresponde a un tiempo de recuperación de referencia de `1 / 0.2 = 5` días. Las tasas `sigma_h` y `sigma_v` representan progresión tras la incubación. Cuando hay salidas competidoras, como progresión y muerte, la permanencia media en el compartimento depende de la suma de sus tasas.

## 4 Parámetros que varían

Los nueve parámetros se muestrean con distribución uniforme dentro de los siguientes intervalos de `dengue.txt`:

| Parámetro | Significado | Nominal | Mínimo | Máximo | Unidad |
| --- | --- | ---: | ---: | ---: | --- |
| `b` | Picaduras por mosquito y día | 0.6 | 0.3 | 1.0 | día⁻¹ |
| `beta_h` | Probabilidad de transmisión mosquito a humano | 0.5 | 0.2 | 0.75 | Sin dimensión |
| `beta_v` | Probabilidad de transmisión humano a mosquito | 0.5 | 0.2 | 0.75 | Sin dimensión |
| `sigma_h` | Progresión de expuesto a infeccioso humano | 0.1667 | 0.1429 | 0.25 | día⁻¹ |
| `gamma_h` | Recuperación humana | 0.2 | 0.1429 | 0.3333 | día⁻¹ |
| `sigma_v` | Progresión de expuesto a infeccioso del mosquito | 0.1 | 0.0714 | 0.1667 | día⁻¹ |
| `mu_v` | Mortalidad natural del mosquito | 0.0714 | 0.0476 | 0.1429 | día⁻¹ |
| `m` | Mosquitos basales por humano | 2.5 | 1.0 | 4.0 | Razón |
| `u` | Mortalidad adicional del vector por control | 0.02 | 0 | 0.05 | día⁻¹ |

La tasa humana `mu_h = 0.0000391` por día permanece fija. El muestreo hace variar conjuntamente los nueve parámetros; el nominal no sustituye las combinaciones LHS.

Estos son rangos de exploración del proyecto. El avance reconoce que requieren justificación bibliográfica. Además, asumir uniforme una tasa no equivale a asumir uniforme su tiempo inverso: una distribución uniforme de `sigma_h` induce otra distribución sobre `1 / sigma_h`.

## 5 Ecuaciones y significado

Las fuerzas de infección son tasas de exposición por susceptible:

```text
lam_h = b × beta_h × m × ivr
lam_v = b × beta_v × ih
```

Por ejemplo, `lam_h × sh` es el flujo de humanos susceptibles a expuestos, expresado como fracción de la población por día.

Las ecuaciones humanas son:

```text
sh' = mu_h − lam_h × sh − mu_h × sh
eh' = lam_h × sh − (sigma_h + mu_h) × eh
ih' = sigma_h × eh − (gamma_h + mu_h) × ih
rh' = gamma_h × ih − mu_h × rh
ch' = sigma_h × eh
```

El apóstrofo indica derivada respecto del tiempo. Cada ecuación suma entradas y resta salidas. Al sumar las primeras cuatro, se obtiene `H' = mu_h × (1 − H)`. Como `H(0) = 1`, la población humana normalizada se conserva.

Las ecuaciones del mosquito son:

```text
svr' = mu_v − lam_v × svr − (mu_v + u) × svr
evr' = lam_v × svr − (sigma_v + mu_v + u) × evr
ivr' = sigma_v × evr − (mu_v + u) × ivr
```

El reclutamiento de mosquitos es constante e igual a `mu_v` en unidades basales. Para `V = svr + evr + ivr`, resulta:

```text
V' = mu_v − (mu_v + u) × V
V de equilibrio = mu_v / (mu_v + u)
```

Cuando `u > 0`, la población de mosquitos disminuye desde su valor inicial `V(0) = 1` hacia un equilibrio menor. En esta implementación, el control actúa como mortalidad adicional constante; no hay un mecanismo separado de reducción de criaderos o de picaduras.

### Condiciones iniciales y escalas temporales

El modelo empieza con `sh = 0.999`, `ih = 0.001`, `svr = 1`, y los demás estados en cero. Se simulan 365 días con Runge–Kutta de cuarto orden y paso de integración de 0.05 días. Se guardan salidas cada 5 días.

Son tres resoluciones distintas: integración cada 0.05 días, almacenamiento cada 5 días y cálculo de PRCC cada N filas almacenadas. Con el N predeterminado de 3, los PRCC guardados aparecen espaciados aproximadamente 15 días. Aumentar N reduce los puntos de PRCC, sin modificar el paso del integrador.

### Interpretación de R0 y una inconsistencia pendiente

El código calcula:

```text
R0_codigo² = b² × beta_h × beta_v × m × sigma_h × sigma_v
            / [(gamma_h + mu_h) × (sigma_h + mu_h)
               × (mu_v + u) × (sigma_v + mu_v + u)]
```

Ese valor es constante durante cada trayectoria porque solo depende de parámetros. No es un número reproductivo efectivo que se actualice con los susceptibles.

Hay una diferencia entre esta fórmula y el umbral obtenido al linealizar las ecuaciones en su equilibrio libre de infección con control permanente. En ese equilibrio, `sh = 1` y `svr = mu_v / (mu_v + u)`. La transmisión hacia los mosquitos incluye ese último factor; por tanto, con la misma convención de raíz cuadrada:

```text
R0_equilibrio = R0_codigo × sqrt(mu_v / (mu_v + u))
```

Esta relación se deduce de las ecuaciones implementadas. Ambos valores coinciden cuando `u = 0`. Para `u > 0`, el valor del código corresponde a evaluar el factor de susceptibilidad vectorial en su nivel basal, en lugar del equilibrio bajo control.

Esto afecta la interpretación de `R0 > 1` y el subconjunto que Python utiliza para analizar el día del pico. Antes de presentar ese filtro como clasificación epidémica, debe definirse qué número reproductivo se desea y reconciliarlo con el modelo. Cambiar la fórmula exige regenerar los resultados correspondientes; esta guía describe los resultados actuales sin modificarlos.

## 6 Cómo funciona el análisis de sensibilidad

### Muestreo de hipercubo latino

LHS significa Latin Hypercube Sampling. Para cada parámetro, se divide su distribución en 999 estratos de igual probabilidad y se combina una selección de cada estrato con las selecciones de los demás parámetros. Así se cubre cada rango marginal sin recorrer todas las combinaciones de una cuadrícula de nueve dimensiones.

Cada fila conceptual de la matriz representa un escenario con nueve valores y produce una trayectoria completa. En el archivo `lhsmatrix`, los parámetros están almacenados por filas; Python transpone la lectura para obtener una matriz de forma `(999, 9)`.

La semilla configurada es `20261118`. Deben conservarse semilla, orden de parámetros, rangos y herramientas para reproducir el experimento. Un tamaño de 999 muestras es una configuración del estudio y el máximo documentado para esta herramienta; por sí solo no demuestra convergencia del análisis.

### Correlación parcial de rangos

El PRCC mide la asociación entre los rangos de un parámetro y los rangos de una salida tras ajustar por los otros parámetros. Una manera de entenderlo es quitar de ambos rangos la parte explicada linealmente por los demás y correlacionar los residuos.

Python lo calcula mediante la inversa de la matriz de correlaciones de rangos. Los empates reciben rangos promedio.

| PRCC | Lectura dentro del experimento |
| --- | --- |
| Cercano a +1 | Valores mayores del parámetro se asocian fuertemente con salidas mayores |
| Cercano a −1 | Valores mayores se asocian fuertemente con salidas menores |
| Cercano a 0 | Asociación monotónica parcial débil |

Un PRCC de 0.9 no significa que aumentar un parámetro 1 % aumente la salida 90 %, ni que explique 90 % de la variabilidad. Tampoco permite comparar directamente la rentabilidad de intervenciones.

El método es más informativo para relaciones monotónicas: al aumentar la entrada, la salida tiende a moverse en una dirección. Una relación en U puede tener PRCC pequeño y aun así mostrar una dependencia fuerte. Conviene revisar gráficos de dispersión antes de interpretar un coeficiente pequeño como falta de influencia.

### Valores p y salidas constantes

Python usa una prueba t aproximada con `n − k − 1` grados de libertad: n muestras y k parámetros. Para 999 muestras y nueve parámetros son 989 grados de libertad.

Un valor p pequeño indica evidencia de asociación en esa prueba bajo sus supuestos. El script marca `p < 0.05` sin corregir por las múltiples pruebas entre parámetros, salidas y tiempos. Los ceros del CSV pueden ser valores extremadamente pequeños que se redondean o sufren subdesbordamiento numérico.

En el tiempo inicial todos los escenarios comparten condiciones iniciales; varias salidas son constantes y su correlación no está definida. Python devuelve `NaN` cuando la matriz de correlaciones contiene valores no finitos. También puede fallar al invertir una matriz singular, caso que el código no trata explícitamente.

### Por qué cambia el PRCC con el tiempo

La pregunta «qué aumenta los infecciosos al día 30» es distinta de «qué aumenta los infecciosos al día 300». Una transmisión mayor puede adelantar y agrandar la ola, agotar susceptibles antes y dejar menos infecciosos al final. Un cambio de signo temporal puede reflejar ese desplazamiento de la epidemia.

Por eso el script añade salidas escalares: el máximo de `ih`, el día en que ocurre y `ch` al día 365. El llamado «tamaño final» del CSV es el acumulado al terminar ese horizonte; no se comprueba que toda trayectoria haya terminado su dinámica epidémica.

## 7 Flujo técnico completo

```text
dengue.txt
   ↓ teval1 traduce las directivas y ecuaciones
temp1.c
   ↓ gcc compila con las fuentes numéricas del curso
run1
   ↓ genera las muestras y resuelve las ecuaciones
Trayectorias numeradas + archivos lhs*
   ↓ prcc_fix calcula estadísticas y correlaciones
prcc.0001 ... prcc.0004 + gráficos PostScript
   ↓ ps2pdf convierte los gráficos
PDF

La carpeta de salida completa
   ↓ analisis_prcc.py reutiliza las mismas muestras
LSODA + PRCC en Python + comparación + PNG + CSV
```

`lhsrun` usa `prcc_fix` si está disponible y permite escoger otro ejecutable con `PRCC`. Elimina el límite de pila cuando puede y reintenta PRCC con intervalos mayores si falla. El script no usa `set -e` ni `pipefail`: la tubería `./run1 | tail -3` puede ocultar un fallo del simulador. La aparición del mensaje final no basta para certificar una corrida correcta; hay que comprobar datos y registros.

El Dockerfile instala compiladores, C shell, gnuplot, Ghostscript y bibliotecas científicas de Python. Su prueba durante la construcción verifica traducción a C de un ejemplo, no una ejecución completa de dengue.

## 8 Cómo ejecutar el proyecto

Desde la raíz del repositorio en Linux:

```bash
docker build -t lhsprcc .
cp models/dengue.txt scripts/analisis_prcc.py work/
docker run --rm -it -v "$PWD/work:/work" lhsprcc
```

Dentro del contenedor:

```bash
lhsrun ejemplo_sir.txt
lhsrun dengue.txt
python3 analisis_prcc.py out_dengue figuras
```

Las salidas quedan en el equipo anfitrión bajo `work/out_ejemplo_sir/`, `work/out_dengue/` y `work/figuras/`. El volumen conserva los archivos aunque se elimine el contenedor. Para PowerShell, consulta la sintaxis del volumen en `README_DOCKER.md`.

`analisis_prcc.py` necesita los datos originales completos; no funciona entregándole únicamente los archivos `prcc.000*`. Además, está adaptado específicamente al dengue: fija condiciones iniciales, horizonte de 365 días, nueve parámetros, orden de estados y salidas. No es un analizador genérico del SIR.

Para comparar con el ejecutable original, conserva primero una copia separada de la salida corregida. Ejecutar otra vez `lhsrun dengue.txt` reutiliza `out_dengue/` y puede sobrescribir resultados. La comparación automática de Python busca originales en `out_dengue/prcc_original/`; los archivos históricos en results/historicos_dengue/prcc_original no se detectan automáticamente.

### Qué revisar después de ejecutar

Comprueba que `compile.log` no tenga errores, que `prcc.log` informe finalización y que existan las 999 trayectorias de dengue con cinco columnas: tiempo, `ih`, `ivr`, `ch`, `R0`. Revisa que los estados sean físicamente plausibles y que no aparezcan valores no finitos.

Python imprime diferencias máximas entre RK4 y LSODA, y entre los PRCC del software y los independientes. El README documenta diferencias de PRCC de aproximadamente 0.001 o menores tras la corrección; es una referencia previa que debe contrastarse en una corrida nueva. El script imprime discrepancias, pero no impone automáticamente un criterio de aprobación ni verifica `s.success` después de integrar.

## 9 Cómo leer los archivos de resultados

El orden de `$plot` determina la correspondencia:

| Archivo | Salida |
| --- | --- |
| `prcc.0001` | `ih`, humanos infecciosos |
| `prcc.0002` | `ivr`, mosquitos infecciosos respecto de la población basal |
| `prcc.0003` | `ch`, acumulado de nuevas entradas a infecciosos |
| `prcc.0004` | `R0`, fórmula actualmente implementada |

Según el código fuente `my_prcc2.cc` del paquete, las columnas son:

| Columnas desde 1 | Contenido |
| --- | --- |
| 1 | Tiempo |
| 2 a 6 | Media, mediana, varianza, máximo y mínimo |
| 7 y 8 | Límites calculados a partir de media ± 1.96 × desviación estándar / √n, con ajustes del programa |
| 9 y 10 | PRCC y valor p de `b` |
| 11 y 12 | PRCC y valor p de `beta_h` |
| Restantes pares | Los demás parámetros en el orden de `$lhs` |

Los límites de las columnas 7 y 8 parten de una aproximación normal para la incertidumbre de la media mediante su error estándar. El programa reemplaza el límite inferior por la media si resulta negativo y el superior por la media si supera el doble de esta. Esos ajustes alteran el intervalo original. No son los percentiles 5 y 95 ni representan la dispersión de las trayectorias; para esta última, consulta las bandas percentiles de la primera figura.

`fig1_trayectorias.png` presenta mediana y bandas 25–75 % y 5–95 % entre simulaciones. Son distribuciones de escenarios dados los rangos de parámetros, no intervalos de predicción calibrados con datos epidemiológicos.

`fig2_prcc_tiempo.png` presenta los PRCC del software y puntos para sus valores p menores de 0.05. Aunque Python calcula coeficientes independientes para comparar, esa figura utiliza los del software.

`fig3_prcc_outcomes.png` presenta los PRCC calculados en Python para acumulado al día 365, pico y día del pico. El pico se busca sobre una cuadrícula diaria: su momento tiene resolución de un día y puede omitir un máximo entre días.

## 10 Qué muestran los resultados guardados

Los siguientes valores proceden de `prcc_outcomes_escalares.csv`; describen la corrida guardada y sus rangos actuales.

| Parámetro | Acumulado al día 365 | Pico de infecciosos |
| --- | ---: | ---: |
| `b` | +0.9264 | +0.8868 |
| `beta_h` | +0.8037 | +0.6991 |
| `beta_v` | +0.7640 | +0.6812 |
| `sigma_h` | +0.0220 | +0.0850 |
| `gamma_h` | −0.6320 | −0.7250 |
| `sigma_v` | +0.3779 | +0.3451 |
| `mu_v` | −0.7189 | −0.4985 |
| `m` | +0.8023 | +0.7068 |
| `u` | −0.7567 | −0.6024 |

En estas muestras, una mayor tasa de picadura se asocia fuertemente con mayor acumulado y pico. Una recuperación humana más rápida y una mortalidad vectorial mayor se asocian con valores menores. El control `u` también muestra una asociación negativa clara.

`sigma_h` tiene una asociación pequeña con el acumulado y un valor p de 0.49 para esa salida. Para el pico, la asociación sigue siendo pequeña, aunque su valor p es 0.00741. Esto ilustra por qué magnitud y significancia deben leerse por separado.

El análisis del día del pico usa 856 de las 999 muestras, seleccionadas mediante el `R0` del código mayor que uno. Dentro de ese subconjunto, el PRCC de `b` es −0.3697: mayores tasas de picadura se asocian con picos más tempranos. La selección condiciona la población analizada y debe revisarse junto con la definición de R0 explicada antes.

Estos coeficientes no permiten afirmar que una intervención concreta sea la mejor. Faltan costos, factibilidad, magnitudes de cambio alcanzables y una representación de cada intervención. Además, cambiar los rangos de entrada puede cambiar la clasificación de sensibilidad.

## 11 Corrección del manejo de empates

Los rangos deben tratar correctamente valores repetidos. En `my_prcc2.cc`, el programa original reinicia el campo `rank`, pero no reinicia `tieset` antes de calcular los grupos de empates. Un valor previo o no inicializado puede contaminar esos grupos y alterar el PRCC.

La corrección añade, tras inicializar los rangos:

```cpp
for(i=0; i<nsim; i++) LHSMatrix[k][i].tieset = 0;
```

El Dockerfile aplica esa línea mediante `sed` y compila `prcc_fix`; no aplica directamente el archivo `.patch`. Conserva también el ejecutable original. La corrección afecta el cálculo estadístico, sin cambiar las ecuaciones ni sus trayectorias.

La comparación independiente es útil porque emplea LSODA frente a RK4 y `rankdata` frente al cálculo de rangos del programa del curso. Ambos caminos todavía comparten las hipótesis del modelo y la misma matriz de parámetros.

## 12 Aspectos que debes tener presentes

1. **El SIR contiene un parámetro sin efecto.** `N0` se incluye en LHS, pero `N` se calcula como `S + I + R` y los valores iniciales son fijos. Cambiar `N0` no cambia la dinámica. Un PRCC pequeño distinto de cero puede aparecer por la muestra y el ajuste estadístico; no representa un mecanismo del modelo.
2. **El avance es preliminar.** Describe 300 días y otros rangos; el dengue implementado usa 365 días y los intervalos de esta guía. Parte de sus tareas pendientes ya tiene código o resultados guardados.
3. **El acumulado no es prevalencia.** `ih` indica infecciosos presentes; `ch` suma entradas al estado infeccioso desde el inicio. La incidencia instantánea correspondiente es `sigma_h × eh`.
4. **El modelo simplifica la biología.** No incluye serotipos, inmunidad cruzada, estacionalidad, espacio, edades, movimiento humano ni variación temporal del control. No contiene hospitalizaciones, gravedad clínica o notificación de casos.
5. **La reproducibilidad requiere conservar datos.** La imagen usa una base y paquetes sin fijar cada versión, y el flujo reutiliza carpetas. Conviene archivar modelo, matriz LHS, registros, versiones y resultados juntos.
6. **La verificación completa depende del entorno.** En la revisión de este checkout no se encontró Docker en el PATH y el Python disponible no tiene SciPy. Se inspeccionaron archivos y fuentes del paquete; no se volvió a ejecutar el experimento completo de dengue. Los valores numéricos de la sección anterior son los artefactos guardados.

## 13 Ruta de aprendizaje

| Etapa | Qué dominar | Ejercicio sobre este proyecto |
| --- | --- | --- |
| 1 | Compartimentos y flujos | Explicar por qué un expuesto no transmite y dibujar el ciclo humano–mosquito |
| 2 | Fracciones, unidades y tasas | Convertir `ih = 0.02` a personas para una población de 10 000 y calcular `1 / gamma_h` |
| 3 | Ecuaciones diferenciales | Identificar todas las entradas y salidas de `eh`; comprobar la conservación humana |
| 4 | Integración numérica | Diferenciar paso del integrador, frecuencia de guardado y frecuencia del PRCC |
| 5 | Incertidumbre y LHS | Explicar por qué 999 escenarios no son una cuadrícula de todas las combinaciones |
| 6 | Rangos y correlación parcial | Interpretar signo, magnitud y valor p sin convertir PRCC en porcentaje causal |
| 7 | Lectura de resultados | Comparar PRCC temporal con PRCC del pico y del acumulado |
| 8 | Verificación científica | Separar coincidencia entre implementaciones de validación con datos reales |

Para practicar sin alterar los resultados existentes, copia los modelos con otro nombre y ejecuta el flujo sobre esas copias. Empieza por SIR, identifica el parámetro sin efecto y después pasa a dengue. Antes de cambiar parámetros, escribe qué salida esperas que cambie y por qué; contrasta después esa predicción con las trayectorias y los PRCC.

## 14 Preguntas para comprobar comprensión

- ¿Por qué `ch` no se suma a `sh + eh + ih + rh`?
- ¿Qué diferencia hay entre `ivr` y la fracción infecciosa entre mosquitos vivos?
- ¿Por qué aumentar `u` reduce la población total del vector en estas ecuaciones?
- ¿Cómo puede un parámetro aumentar el pico y reducir los infecciosos en un día tardío?
- ¿Por qué un PRCC pequeño no descarta una relación no monotónica?
- ¿Qué cambia si modificas N en `lhsrun`, y qué cambia si modificas `$timestep`?
- ¿Por qué Python debe usar exactamente las mismas muestras para comparar implementaciones?
- ¿Qué falta para pasar de un experimento de sensibilidad a una predicción local de dengue?

## 15 Archivos para profundizar

Lee primero [dengue.txt](../models/dengue.txt), después [lhsrun](../scripts/lhsrun) y finalmente [analisis_prcc.py](../scripts/analisis_prcc.py). Usa [README_DOCKER.md](README_DOCKER.md) para ejecutar y [prcc_outcomes_escalares.csv](../results/historicos_dengue/figuras/prcc_outcomes_escalares.csv) para contrastar las interpretaciones numéricas.

El [avance del laboratorio](avance_laboratorio.txt) enumera bibliografía sobre modelos de dengue, dinámica de sistemas y sensibilidad global. Es una ruta de lectura posterior; la atribución exacta del modelo y la justificación de los rangos requieren revisar esas publicaciones.
