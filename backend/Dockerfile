FROM python:3.13-slim
RUN useradd -m -u 1000 user
USER user
# Set the working directory inside the container
WORKDIR /home/user/app
ENV PATH="/home/user/.local/bin:$PATH"
# Copy all files from the current directory to the container's working directory
COPY --chown=user . .
# Install dependencies from the requirements file without using cache to reduce image size
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# Start the app with Gunicorn on port 7860
CMD ["gunicorn", "-w", "1", "--timeout", "120", "-b", "0.0.0.0:7860", "app:learn_api"]
