# Informe de dengue en LaTeX

`main.tex` es el documento principal. `informe_dengue.pdf` es la versión compilada.

## Formato

Se utiliza una copia de `MastersDoctoralThesis.cls` de la plantilla proporcionada, sin modificar el original. Se conservan el papel A4, Palatino de 12 puntos, interlineado de 1.5 y los márgenes de la clase: izquierdo 1.5 pulgadas (3.81 cm), derecho 1 pulgada (2.54 cm), superior 0.6 pulgadas e inferior 0.8 pulgadas, con encabezado y pie incluidos según `geometry`.

El documento tiene secciones de informe. No incorpora capítulos de tesis, agradecimientos, dedicatorias ni páginas de relleno. La carátula conserva el bloque original de título, autor, curso, institución y fecha de `docs/entregables/informe_dengue (1).pdf`, en su posición original. El resumen actualizado se mantiene en una página aparte.

La carátula y los diagramas se incorporan como PDF vectoriales, sin redibujar sus elementos. Los campos visibles de la carátula son los del original. `datos_portada.tex` se conserva como archivo de datos del documento; no modifica el PDF de carátula incrustado.

## Compilación

Desde esta carpeta, con TeX Live, pdfLaTeX, BibTeX y latexmk disponibles:

```bash
make
```

O bien:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
cp build/main.pdf informe_dengue.pdf
```

`build/` contiene los archivos auxiliares, registros y las imágenes de revisión. No hace falta para compilar desde cero. Se pueden cargar `main.tex`, `datos_portada.tex`, la clase, la bibliografía y las carpetas `figuras/` y `datos/` en un editor LaTeX; el compilador es pdfLaTeX y el documento principal es `main.tex`.

## Contenido y procedencia

Se mantienen las ecuaciones, rangos y resultados del informe corregido y de `work/mejora_20261120`. Las tablas de PRCC se transcriben del CSV local; el CSV conserva también los valores p. Los diagramas causal y de Forrester son las figuras originales de las páginas 5 y 6, recortadas sin sus pies de figura e incorporadas mediante `includegraphics`. Los pies se componen en LaTeX. `scripts/extraer_originales.py` documenta la extracción con PyMuPDF; no es necesario ejecutarlo para compilar porque los PDF extraídos ya están incluidos. La redacción se revisó con humanizer-es, con tono académico y sin modificar los resultados numéricos.

El cotejo exhaustivo de la fuente de cada límite paramétrico sigue pendiente. Esta limitación aparece en el texto. No se han incorporado cifras epidemiológicas nuevas ni se ha supuesto validación con datos de un brote real.
