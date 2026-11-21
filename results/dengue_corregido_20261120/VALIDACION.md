# Validación de la versión corregida

SIR y dengue ejecutados con la imagen lhsprcc existente, sin cambiar el toolchain. Se conservaron registros de compilación, PRCC y gráficos PDF.

- 999 muestras, semilla 20261118; parámetros de `out_dengue/dengue.txt`.
- R0 nominal corregido: 1.8185; mediana LHS: 1.2543, P5/P95: 0.4327/3.6121; R0>1: 62.8629 %.
- Día del pico: 569 máximos interiores superiores a 2Ih(0); 35 máximos al límite de 365 días.
- LSODA frente a RK4: errores máximos Ih 4.99e-7, Iv 5e-7, Ch 5e-6.
- PRCC con los mismos datos redondeados: diferencias <5e-7. Con trayectorias LSODA sin redondear: diferencias hasta aproximadamente 0.005.
- Original frente a corregido: diferencias máximas Ih 0.004239; Iv 0.017534; Ch 0.127563. Una ejecución del original no garantiza determinismo.
- Los tres escenarios de control pasan conservación humana, balance vectorial, no negatividad y acumulación monótona; errores RK4/LSODA inferiores a 1e-9.
- `diagnosticos/` conserva dispersiones por rangos y salidas numéricas. No se certifica monotonía global mediante la mera generación de esos gráficos.
- PDF renderizado y PPTX renderizado con Artifact Tool. Validación estructural, geométrica y de gráficos nativos en `build/validacion.json`. No se abrió PowerPoint.

Pendientes: identidades académicas y cotejo exhaustivo de cada rango bibliográfico. No hay validación epidemiológica contra un brote real.
