FROM python:3

WORKDIR /project

COPY req.txt req.txt

RUN pip3 install -r req.txt 

COPY . .  

EXPOSE 8000  

CMD ["python", "main.py"]
