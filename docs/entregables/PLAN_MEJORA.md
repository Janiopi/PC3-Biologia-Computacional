# Plan de mejora de los entregables de dengue

1. Sincronizar parámetros, rangos y condiciones iniciales con el informe. Corregir R0 incorporando mu_v/(mu_v+u) en su cuadrado.
2. Regenerar 999 simulaciones con semilla 20261118, RK4 h=0.05 y horizonte de 365 días. Conservar matriz, registros y metadatos en una ejecución nueva.
3. Verificar con LSODA y comparar PRCC sobre datos idénticos antes de estudiar redondeo. Seleccionar el día del pico solo si supera 2Ih(0) y es interior al horizonte.
4. Examinar monotonía, advertir selección y p-valores nominales; comparar controles u=0, 0.05 y 0.15 con los demás parámetros fijos.
5. Verificar bibliografía, retirar cifras sin respaldo y corregir el contador Ch en los diagramas.
6. Regenerar informe PDF y presentación PPTX con fuentes editables. Completar identidades cuando se proporcionen. Repartir problema/modelo y análisis/discusión entre los dos integrantes.
7. Validar SIR, conservación humana, balance vectorial, concordancia numérica y visual de todas las páginas y diapositivas. Preservar originales.

Criterios nominales: R0 aproximadamente 1.82, pico Ih aproximadamente 6.65 % cerca del día 112 y Ch(365) aproximadamente 93.36 %. No ampliar el modelo a calibración, estacionalidad o múltiples serotipos.
