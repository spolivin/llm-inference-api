FROM mybase:torch

ENV USER=appuser
ENV HOME=/home/$USER
RUN useradd -m -d $HOME -s /bin/bash $USER

RUN pip install ctransformers>=0.2.24 prometheus-fastapi-instrumentator

WORKDIR /app
COPY llama_api/ ./llama_api/
RUN chown -R $USER:$USER /app

USER $USER

EXPOSE 8012

CMD ["uvicorn", "llama_api.llama_api:app", "--host", "0.0.0.0", "--port", "8012"]
