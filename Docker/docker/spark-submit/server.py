#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

#curl -i -T input.txt "http://hadoop-server:50010/webhdfs/v1/input.txt?user.name=root&op=CREATE&overwrite=false
class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def _set_headers_json(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def _refuse_request(self):
        self.send_response(404)
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        ret = subprocess.run(args=["/spark/bin/spark-submit", 
                                "--class", "TextSimilarity",
                                "--master", "spark://spark-master:7077", 
                                "--files", "/spark-data/input.txt", 
                                "--deploy-mode", "client",
                                "textsimilarity.jar"],
                                stdout=subprocess.PIPE) #/spark/bin/spark-submit --master spark://spark-master:7077 text_similarity_tf.py
        
        #ret = subprocess.run(args=["/spark/bin/spark-submit", "--master", "spark://master:7077", "text_similarity_tf.py"],
        #                        stdout=subprocess.PIPE) #$SPARK_HOME/sbin/spark-submit --master spark://master:7077 text_similarity_tf.py
        output = ret.stdout
        print("Apache Spark is done")
        print("result: " + output.decode('utf-8'))
        self.wfile.write(output)

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        self._set_headers()
        content_len = int(self.headers.get('Content-Length'))
        text_file = open("/spark-data/input.txt", "w")
        text_file.write(self.rfile.read(content_len).decode('utf-8'))
        text_file.close()
        ret = subprocess.run(args=["/spark/bin/spark-submit", 
                                "--class", "TextSimilarity",
                                "--master", "spark://spark-master:7077", 
                                "--files", "/spark-data/input.txt", 
                                "--deploy-mode", "client",
                                "textsimilarity.jar"],
                                stdout=subprocess.PIPE) #/spark/bin/spark-submit --master spark://spark-master:7077 text_similarity_tf.py
        
        #ret = subprocess.run(args=["/spark/bin/spark-submit", "--master", "spark://master:7077", "text_similarity_tf.py"],
        #                        stdout=subprocess.PIPE) #$SPARK_HOME/sbin/spark-submit --master spark://master:7077 text_similarity_tf.py
        output = ret.stdout
        print("Apache Spark is done")
        print("result: " + output.decode('utf-8'))
        self.wfile.write(output)
        
def run(server_class=HTTPServer, handler_class=Handler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

#spark-submit --class TextSimilarity --master spark://master:7077 textsimilarity.jar