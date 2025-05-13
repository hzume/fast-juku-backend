ARG UV_VERSION=0.6.14
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

FROM public.ecr.aws/lambda/python:3.11

COPY --from=uv /uv /uvx /bin/
COPY pyproject.toml uv.lock ${LAMBDA_TASK_ROOT}/
COPY api/ ${LAMBDA_TASK_ROOT}/api/
ENV PATH /root/.local/bin:$PATH

RUN uv sync

WORKDIR ${LAMBDA_TASK_ROOT}

# Command can be overwritten by providing a different command in the template directly.
CMD ["api.main.lambda_handler"]
