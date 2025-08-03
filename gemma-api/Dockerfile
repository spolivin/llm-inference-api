FROM mybase:torch

ENV USER=appuser
ENV HOME=/home/$USER
RUN useradd -m -d $HOME -s /bin/bash $USER

RUN pip install prometheus-fastapi-instrumentator

WORKDIR /app
COPY gemma_api/ ./gemma_api/
RUN chown -R $USER:$USER /app

USER $USER

EXPOSE 8005

CMD ["uvicorn", "gemma_api.gemma_api:app", "--host", "0.0.0.0", "--port", "8005"]
