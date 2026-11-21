# Entregables corregidos

El informe final está en `informe/main.tex` y `informe/informe_dengue.pdf`. Conserva la carátula y los dos primeros diagramas originales. La carpeta incluye las fuentes LaTeX, bibliografía, figuras y datos necesarios para compilar.

El informe original se conserva en `../informe_dengue (1).pdf`. Estas son las dos únicas versiones del informe. Las presentaciones se mantienen por separado.

Los archivos originales permanecen intactos. El informe y la presentación nuevos utilizan la ejecución `work/mejora_20261120`.

## Evidencia

- `analisis_identico.log`: comparación curso/Python con trayectorias idénticas (error PRCC menor de 5e-7) y comparación independiente LSODA (diferencias hasta 0.005 por redondeo).
- `diagnosticos/metadatos.json`: semillas, selección, tamaños muestrales y comparación controlada.
- `diagnosticos/*.png`: dispersiones por rangos para revisar monotonía; su generación no certifica por sí sola que todas las relaciones sean monótonas.
- `figuras/prcc_outcomes_escalares.csv`: resultados completos con valores p nominales.
- `sir.log`, `dengue.log`, `out_*/compile.log`, `out_*/prcc.log`: registros del software del curso.

## Pendientes antes de la entrega académica

Faltan nombres de ambos integrantes, universidad y docente. La verificación exhaustiva de la procedencia de cada límite bibliográfico no está completada: los rangos se declaran como escenarios asumidos, sin afirmar validación local. La cifra epidemiológica no corroborada se retiró. El informe corregido es una reestructuración del original y mantiene un alcance académico sin calibración.

## Exposición

Integrante 1: diapositivas 1–8 (problema, modelo y solución). Integrante 2: 9–16 (LHS/PRCC, interpretación y fuentes). Ensayar juntos la diferencia entre verificación numérica y validación epidemiológica.

La matriz LHS y los registros numéricos conservados en Git están en `results/dengue_corregido_20261120`.
