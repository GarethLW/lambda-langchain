FROM public.ecr.aws/lambda/python:3.11

# Install runtime dependencies
COPY requirements.txt  ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also use a custom bootstrap for ASGI apps)
CMD ["handler.lambda_handler"]
