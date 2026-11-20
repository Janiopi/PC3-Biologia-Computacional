# Modelo de dengue y análisis LHS PRCC

Simulación de transmisión humano–mosquito y análisis de sensibilidad de nueve parámetros. El entorno Docker incluye el software del curso y la verificación independiente con SciPy.

## Documentación

- [Guía del proyecto](docs/GUIA_PROYECTO.md): modelo, conceptos e interpretación.
- [Guía de ejecución](docs/GUIA_EJECUCION.md): instrucciones explicadas para Linux y Windows.
- [Notas de Docker](docs/README_DOCKER.md).
- [Resultados conservados](results/README.md).

## Organización

| Carpeta | Contenido |
| --- | --- |
| `docs/` | Guías y avance del laboratorio |
| `models/` | Modelos dengue y SIR |
| `scripts/` | Automatización y análisis Python |
| `vendor/` | Paquete original del curso y parche documentado |
| `results/` | Corridas existentes y resultados históricos |
| `work/` | Nuevas ejecuciones y volumen del contenedor |

## Ejecución desde la raíz

En Bash, crea una carpeta nueva; si ya existe, elige otro nombre antes de continuar:

```bash
docker build -t lhsprcc .
mkdir -p work
mkdir work/ejecucion_01
cp models/*.txt scripts/analisis_prcc.py work/ejecucion_01/
docker run --rm -it -v "$PWD/work:/work" lhsprcc
```

Dentro del contenedor:

```bash
cd /work/ejecucion_01
lhsrun ejemplo_sir.txt
lhsrun dengue.txt
python3 analisis_prcc.py out_dengue figuras
exit
```

Los resultados nuevos quedan en `work/ejecucion_01/`. Consulta la guía antes de repetir una corrida para evitar sobrescribirla.

## Modelo causal y dinámico

Consulta la [guía con diagramas editables y simulación independiente](docs/MODELO_CAUSAL_DINAMICO.md).
