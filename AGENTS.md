# Repository Guidelines

## Project Structure & Module Organization

This repository models dengue transmission and performs Latin hypercube sampling (LHS) and partial rank correlation coefficient (PRCC) analysis.

- `models/dengue.txt` defines the human–mosquito model; `models/ejemplo_sir.txt` provides a smaller SIR example.
- `lhsrun` translates models into C, compiles simulations, calculates PRCC, and converts plots to PDF.
- `scripts/analisis_prcc.py` independently solves the dengue model with SciPy and produces comparison figures and CSV results.
- `Dockerfile` installs the toolchain from `vendor/lhsprcc_minimum_tar.gz` and builds the corrected `prcc_fix` executable.
- `work/` holds container inputs and generated `out_<model>/` directories. Existing runs and historical analysis artifacts are preserved under `results/`. Documentation lives in `docs/`; scripts in `scripts/`; model inputs in `models/`; upstream dependencies in `vendor/`.
- `docs/README_DOCKER.md` documents setup, model constraints, and the tieset correction.

## Build, Test, and Development Commands

Run these commands from the repository root on Linux:

```bash
docker build -t lhsprcc .
docker run --rm -it -v "$PWD/work:/work" lhsprcc
```

Inside the container, `lhsrun ejemplo_sir.txt` runs the sample workflow. For dengue analysis, first copy `models/dengue.txt` and `scripts/analisis_prcc.py` into `work/`, then run:

```bash
lhsrun dengue.txt
python3 analisis_prcc.py out_dengue figuras
```

Outputs go to `out_dengue/` and `figuras/`. Use `PRCC=prcc lhsrun dengue.txt` when explicitly comparing the original executable.

## Coding Style & Naming Conventions

Use four spaces for Python indentation, snake_case for functions and local variables, and uppercase names for constants. Preserve the existing Bash style and quote path expansions. No formatter or linter configuration is provided. Model files use `$` directives, semicolon-terminated equations, and `//` comments. Keep parameter ordering synchronized with `PARAMS` in the Python analysis.

## Testing Guidelines

There is no standalone automated test suite or coverage requirement. The Docker build smoke-tests model translation. After workflow changes, run the SIR example and inspect `compile.log`, `prcc.log`, and generated PDFs. After dengue model changes, run the independent Python comparison; investigate deviations from the documented PRCC agreement of approximately 0.001. Preserve seeds and sampling settings for reproducibility.

## Commit & Pull Request Guidelines

Git history is unavailable in this checkout, so no existing commit convention can be verified. Use concise, imperative commit subjects. Pull requests should describe the scientific or workflow change, list validation commands and numerical comparisons, and include updated figures when results change. Identify intentionally regenerated artifacts and link related issues when available.
