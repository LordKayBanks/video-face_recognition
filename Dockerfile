FROM animcogn/face_recognition:cpu

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r ./requirements.txt


# Command to run when the container starts
# This will be overridden by the command-line arguments when running the container
CMD [ "python3", "/app/script.py" ]