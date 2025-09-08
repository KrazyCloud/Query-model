#DockerFile 
FROM python:3.12.3-slim

#set working directory 
WORKDIR /app

#install dependencies 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copy all project files 
COPY . .

#expose FastAPI port(9002)
EXPOSE 9000

#start FastAPI server on port 9002
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9000"]