FROM python:3.10.5
WORKDIR /imsr_project
ADD . /imsr_project
COPY requirements.txt /imsr_project
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install ibm_db
EXPOSE 5000
CMD ["python","runweb.py"]