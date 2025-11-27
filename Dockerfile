FROM python:3.14-slim

WORKDIR /usr/src/app
COPY pyproject.toml uv.lock requirements.txt ./
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV BLOB_READ_WRITE_TOKEN="your_token_here"
EXPOSE 5000
CMD ["flask", "--app", "api", "run", "--host", "0.0.0.0"]