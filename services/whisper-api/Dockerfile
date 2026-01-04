FROM mybase:torch

ENV USER=appuser
ENV HOME=/home/$USER
RUN useradd -m -d $HOME -s /bin/bash $USER

RUN pip install prometheus-fastapi-instrumentator

WORKDIR /app
COPY whisper_api/ ./whisper_api/
RUN chown -R $USER:$USER /app

USER $USER

EXPOSE 8035

CMD ["uvicorn", "whisper_api.whisper_api:app", "--host", "0.0.0.0", "--port", "8035"]
