# LHS/PRCC del curso en Docker (Windows 11)

No necesitas interfaz gráfica ni instalar csh, gnuplot o gcc en Windows: todo corre dentro del contenedor
y los resultados (PDF, archivos de datos) quedan en una carpeta normal de Windows.

## 1. Una sola vez
1. Instala **Docker Desktop** (con backend WSL 2). Es gratuito para uso personal y educativo.
2. Clona el repositorio y entra en su raíz. Conserva la estructura de carpetas:
   - `Dockerfile`
   - `scripts/lhsrun`
   - `vendor/lhsprcc_minimum_tar.gz`
   - `models/`
3. En PowerShell prepara una ejecución nueva:

    New-Item -ItemType Directory -Path work/ejecucion_01
    Copy-Item models/*.txt work/ejecucion_01/
    Copy-Item scripts/analisis_prcc.py work/ejecucion_01/

Si esa carpeta ya existe, usa otro nombre para preservar sus resultados.

## 2. Construir la imagen (PowerShell, en la raíz del repositorio)
    docker build -t lhsprcc .

## 3. Ejecutar
    docker run --rm -it -v "${PWD}\work:/work" lhsprcc

Dentro del contenedor, entra en la carpeta preparada:

    cd /work/ejecucion_01

Luego ejecuta:

    lhsrun ejemplo_sir.txt        # flujo completo: compila, simula con LHS, PRCC, figuras
    crun ejemplo_sir.txt          # alternativa: el crun original del profesor (solo simula)
    prcc 2                        # PRCC a mano, dentro de la carpeta de salida

Los resultados aparecen en `work/ejecucion_01/out_ejemplo_sir/` (abre los `.pdf` con Windows):
`prccvals.pdf` (PRCC vs tiempo), `signif.pdf` (significancia), `output1.pdf`/`stats.pdf`, y los
archivos de texto `prcc.0001, prcc.0002...` (uno por variable de salida).

## Formato de los archivos prcc.NNNN
Columna 1 = tiempo; columnas 2-8 = estadísticos de la variable de salida; desde la columna 9, pares
(PRCC, p-valor) por parámetro en el orden de `$lhs`.

## Notas
- `$lhs N p1 p2 ...;` necesita al menos 2 parámetros para que `prcc` funcione.
- Parámetro con rango uniforme: `p = nominal min min max $U;`  (triangular: `p = nominal min moda max $T;`)
- `prcc N` calcula el PRCC cada N filas de tiempo y guarda sus matrices en la pila de memoria. `lhsrun` quita el límite de pila y, si aun así falla, reintenta con N mayor (5, 10, 20).
- El software acepta como máximo 999 muestras LHS (`$lhs 999 ...`).
- Un valor inicial no puede depender de un parámetro; si lo necesitas, reescala las variables.
- Los métodos `$BSStepPoly/$BSStepRational` no compilan con gcc moderno (el `crun` original tampoco los incluye);
  usa `$Rk4` (obligatorio para LHS) o `$StiffRosenbrock`.

## Modelo de dengue y análisis
Copia `dengue.txt` y `analisis_prcc.py` a `work\` y, dentro del contenedor:

    lhsrun dengue.txt                              # 999 corridas LHS + PRCC (software del curso)
    python3 analisis_prcc.py out_dengue figuras    # verificación independiente + figuras PNG

`analisis_prcc.py` resuelve en Python las mismas 999 combinaciones de parámetros, calcula su propio PRCC,
lo compara con el del software y genera `figuras/fig1..fig3` y `prcc_outcomes_escalares.csv`.

## Sobre prcc_fix (importante)
En `my_prcc2.cc` el campo `tieset` (control de empates) no se reinicia entre pasos de tiempo. Cuando hay
valores repetidos (variables saturadas, p. ej. casos acumulados), el PRCC del `prcc` original sale
atenuado y su error cambia entre ejecuciones (memoria sin inicializar). `prcc_fix` es el mismo programa con
una línea añadida (ver `vendor/prcc_tieset.patch`); coincide con el cálculo independiente en Python (dif. <= 0.001).
`lhsrun` usa `prcc_fix` por defecto; para forzar el original: `PRCC=prcc lhsrun modelo.txt`.
