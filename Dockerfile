FROM python:3.11


WORKDIR /rpgram_setups

COPY ./requirements.txt /rpgram_setups/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /rpgram_setups/requirements.txt

COPY ./src /src
WORKDIR /src

CMD ["uvicorn", "--factory", "rpgram_setup.main:create_app", "--host", "0.0.0.0", "--port", "8001", "--no-access-log"]