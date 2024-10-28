# Use the official AWS Lambda Python runtime as a base image
FROM public.ecr.aws/lambda/python:3.8

# Install the psycopg2 library
RUN yum -y install postgresql-devel gcc && \
    pip install psycopg2 -t .

# Copy the function code into the container
COPY lambda_function.py .

# Command to run the Lambda function
CMD ["lambda_function.lambda_handler"]
