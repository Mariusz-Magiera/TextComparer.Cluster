FROM spark-base:2.3.1

COPY server.py /
COPY textsimilarity.jar /

ENV SPARK_MASTER_URL="spark://spark-master:7077"

COPY input.txt /spark-data/
#RUN touch /input.txt

CMD ["python3", "server.py"]
