FROM public.ecr.aws/lambda/python:3.11

COPY poetry.lock pyproject.toml ${LAMBDA_TASK_ROOT}/
COPY api/ ${LAMBDA_TASK_ROOT}/api/
ENV PATH /root/.local/bin:$PATH

RUN curl -sSL https://install.python-poetry.org | python3 - 

RUN poetry config virtualenvs.create false --local
RUN poetry install --no-root

WORKDIR ${LAMBDA_TASK_ROOT}

# Command can be overwritten by providing a different command in the template directly.
CMD ["api.main.lambda_handler"]
