FROM python:3.8


#Create a folder /app  if it doesn't exist
# the /app folder is the current working directory
WORKDIR /app

# Copy necessary files to our app
COPY ./main.py  /app

COPY  ./requirements.txt /app

# announcement
EXPOSE 30000 

# Disable pip cache to shirk the image size a little bit
# since it does not need to be re-installed
RUN pip install -r requirements.txt --no-cache-dir

CMD [ "uvicorn", "main:app","--host", "0.0.0.0", "--port", "30000" ]