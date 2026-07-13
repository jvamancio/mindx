# syntax=docker/dockerfile:1

# =========================================================
# Stage 1: builder — resolve e instala as dependências com uv
# =========================================================
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0

# Instala as dependências primeiro (sem o código-fonte) para
# maximizar o cache de camadas — só reinstala se uv.lock/pyproject mudarem
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# Agora copia o código-fonte e instala o próprio projeto
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

# =========================================================
# Stage 2: runtime — imagem final, enxuta e sem ferramentas de build
# =========================================================
# Mesma suíte Debian (trixie) da imagem do builder: evita mismatch de
# glibc/ABI entre os binários compilados na venv e a imagem final
FROM python:3.13-slim-trixie AS runtime

# Usuário não-root — criado só na imagem final, que é a que roda em produção
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home --no-log-init nonroot

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Copia SOMENTE a venv pronta + código da app do builder.
# Nada de uv, cache, compiladores ou pyproject/uv.lock na imagem final.
COPY --from=builder --chown=nonroot:nonroot /app /app

# A imagem base do uv injeta um ENTRYPOINT que invoca `uv`;
# como aqui não usamos mais uv, resetamos
ENTRYPOINT []

USER nonroot

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

# Produção: chama o binário da venv diretamente (fastapi run, sem reload).
# Evita `uv run`, que faria sync/relink em runtime — desnecessário aqui
# (deps já resolvidas no build) e é justamente uma causa comum do erro
# "no such file or directory" quando a venv não bate com a imagem final.
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]