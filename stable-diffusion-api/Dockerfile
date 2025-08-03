FROM mybase:torch

ENV USER=appuser
ENV HOME=/home/$USER
RUN useradd -m -d $HOME -s /bin/bash $USER

RUN pip install prometheus-fastapi-instrumentator

WORKDIR /app
COPY stable_diffusion_api/ ./stable_diffusion_api/
RUN chown -R $USER:$USER /app

ENV HF_HOME=/app/.cache/huggingface
RUN mkdir -p $HF_HOME && chown -R $USER:$USER $HF_HOME

USER $USER

EXPOSE 8015

CMD ["uvicorn", "stable_diffusion_api.main:app", "--host", "0.0.0.0", "--port", "8015"]
