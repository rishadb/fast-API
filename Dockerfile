#refer docker hub python page

#python image from docker hub
FROM python:3.9.7 

#optional step: set working dir in python img to store the app codes
WORKDIR /usr/src/app



#copy requirements.txt from local to docker container directory ./ = WORKDIR
#copying req is significant here coz docker make container as layers from this page and store the result as cache. if a change is made, docker look for each layer cache and compare the change.
#copying and running req here will save us from running this step for a "change in code only and not req.txt". 
COPY requirements.txt ./

#install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

#copy everything in current local dir to current container dir . = WORKDIR
COPY . .

#command to run to start the container. command is seperated for spaces and put in a list
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


#docker build -t imageName . - to make the docker image in CLI, . - for dockerfile context