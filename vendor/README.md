# Dependencias del curso

`lhsprcc_minimum_tar.gz` es el paquete original del software LHS/PRCC proporcionado en el curso. Se conserva sin modificar para construir el entorno Docker. La autoría y los permisos del paquete corresponden a sus titulares; este repositorio no le asigna una licencia nueva.

`prcc_tieset.patch` documenta el reinicio de empates en `my_prcc2.cc`. El Dockerfile aplica esa corrección al compilar `prcc_fix` y conserva el ejecutable original para comparaciones. Consulta [las notas de Docker](../docs/README_DOCKER.md).
