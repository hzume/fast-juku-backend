FROM public.ecr.aws/lambda/python:3.11

COPY api poetry.lock pyproject.toml ${LAMBDA_TASK_ROOT}/
ENV PATH /root/.local/bin:$PATH

RUN curl -sSL https://install.python-poetry.org | python3 - 

RUN poetry config virtualenvs.create false --local
RUN poetry install --no-root

# Command can be overwritten by providing a different command in the template directly.
CMD ["main.lambda_handler"]
