# Entorno reproducible para el software LHS/PRCC del curso (teval1 + crun + prcc)
# No requiere interfaz gráfica: gnuplot escribe directamente a .ps/.pdf.
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc g++ libc6-dev csh gnuplot-nox ghostscript graphviz \
        python3 python3-numpy python3-scipy python3-pandas python3-matplotlib \
    && rm -rf /var/lib/apt/lists/*

# El software del docente (el .tar.gz se conserva en vendor/)
COPY vendor/lhsprcc_minimum_tar.gz /tmp/
RUN tar -xzf /tmp/lhsprcc_minimum_tar.gz -C /tmp \
 && mkdir -p /usr/local/intode \
 && cp -r /tmp/lhsprcc_minimum/src /tmp/lhsprcc_minimum/test /usr/local/intode/ \
 && cp /tmp/lhsprcc_minimum/teval1 /tmp/lhsprcc_minimum/prcc \
       /tmp/lhsprcc_minimum/crun /tmp/lhsprcc_minimum/icrun /usr/local/bin/ \
 && chmod 755 /usr/local/bin/teval1 /usr/local/bin/prcc /usr/local/bin/crun /usr/local/bin/icrun

# prcc_fix = prcc del profesor + una linea que reinicia los empates ("tieset") en cada paso de tiempo.
# El prcc original queda intacto. Ver prcc_tieset.patch y la seccion de verificacion del informe.
RUN cd /tmp/lhsprcc_minimum/src \
 && sed -i '/LHSMatrix\[k\]\[i\].rank = 1.0;/a\ for(i=0; i<nsim; i++) LHSMatrix[k][i].tieset = 0;' my_prcc2.cc \
 && g++ my_prcc2.cc betai.c gammln.c betacf.c nrutil.c -lm -O2 -o /usr/local/bin/prcc_fix \
 && chmod 755 /usr/local/bin/prcc_fix \
 && rm -rf /tmp/lhsprcc_minimum /tmp/lhsprcc_minimum_tar.gz

# Script de flujo completo (modelo -> LHS -> PRCC -> PDF). sed quita saltos de línea de Windows (CRLF)
COPY scripts/lhsrun /usr/local/bin/lhsrun
RUN sed -i 's/\r$//' /usr/local/bin/lhsrun && chmod 755 /usr/local/bin/lhsrun

# Prueba de humo en la construcción: teval1 debe poder traducir un modelo de ejemplo
RUN cd /tmp && teval1 < /usr/local/intode/test/test12.txt && test -f temp1.c && rm -f temp1.c *.gp lhs* plot.scr

WORKDIR /work
CMD ["bash"]
