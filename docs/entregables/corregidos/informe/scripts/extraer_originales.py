"""Extrae el bloque de carátula y los diagramas del PDF original sin redibujarlos.

Ejecutar desde cualquier carpeta con PyMuPDF disponible. Los PDF resultantes
conservan los trazos vectoriales. Las coordenadas están en puntos PDF.
"""
from pathlib import Path
import pymupdf

REPORT = Path(__file__).resolve().parents[1]
SOURCE = REPORT.parents[1] / 'informe_dengue (1).pdf'
def recortar(original, index, clip, destination, full_page=False):
    # Eliminar también el texto fuera del recorte para evitar que aparezcan
    # el resumen antiguo o pies duplicados al seleccionar o extraer texto.
    clean = pymupdf.open()
    clean.insert_pdf(original, from_page=index, to_page=index)
    source_page = clean[0]
    width, height = source_page.rect.width, source_page.rect.height
    for rect in [pymupdf.Rect(0, 0, width, clip.y0),
                 pymupdf.Rect(0, clip.y1, width, height),
                 pymupdf.Rect(0, clip.y0, clip.x0, clip.y1),
                 pymupdf.Rect(clip.x1, clip.y0, width, clip.y1)]:
        if not rect.is_empty:
            source_page.add_redact_annot(rect, fill=False)
    source_page.apply_redactions(images=2, graphics=1, text=0)
    output = pymupdf.open()
    page = output.new_page(width=width if full_page else clip.width,
                           height=height if full_page else clip.height)
    target = clip if full_page else page.rect
    page.show_pdf_page(target, clean, 0, clip=clip)
    output.save(destination, garbage=4, deflate=True)
    output.close()
    clean.close()


with pymupdf.open(SOURCE) as original:
    recortar(original, 0, pymupdf.Rect(0, 0, original[0].rect.width, 310),
             REPORT / 'figuras/caratula_original.pdf', full_page=True)
    for name, index, bounds in [
        ('diagrama_causal_original.pdf', 4, (70, 100, 526, 399)),
        ('diagrama_forrester_original.pdf', 5, (70, 302, 526, 574)),
    ]:
        recortar(original, index, pymupdf.Rect(bounds), REPORT / 'figuras' / name)
