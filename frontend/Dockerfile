FROM python:3.13-slim
RUN useradd -m -u 1000 user
USER user
WORKDIR /home/user/app
ENV PATH="/home/user/.local/bin:$PATH"
COPY --chown=user . .
RUN pip3 install -r requirements.txt
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
