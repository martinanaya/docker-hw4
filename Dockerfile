FROM --platform=linux/amd64 python
WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY reqs.txt reqs.txt
RUN pip install -r reqs.txt
COPY . .
CMD ["flask","run"]
