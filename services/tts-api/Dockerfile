FROM mybase:torch

ENV USER=appuser
ENV HOME=/home/$USER
RUN useradd -m -d $HOME -s /bin/bash $USER

RUN pip install soundfile prometheus-fastapi-instrumentator

WORKDIR /app
COPY tts_api/ ./tts_api/
RUN chown -R $USER:$USER /app

USER $USER

EXPOSE 8025

CMD ["uvicorn", "tts_api.tts_api:app", "--host", "0.0.0.0", "--port", "8025"]
