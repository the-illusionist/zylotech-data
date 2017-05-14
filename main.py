###############################################################

# To run:
# /usr/local/spark/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.0.0 ~/workspace/personal/zylotech/main.py

# Sample request:
# {
# 	"filters":["a","c"]
# }

# Sample response:
# {'avgZ': 520511.71428571426, 'sumX': 2342383.0}

################################################################

from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse, json

from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import functions as F
# from pyspark.sql.functions import broadcast

sc_conf = SparkConf()
sc_conf.set("spark.mongodb.output.uri","mongodb://127.0.0.1//db.coll")
sc = SparkContext(conf=sc_conf)
sqlContext = SQLContext(sc)

# Loading data from products collection in spark dataframe using mongo-spark connector
dfp = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri",
    "mongodb://127.0.0.1/test.product3").load()

# ordering the dfp using Y led to a slower performance
# dfp = dfp.orderBy(dfp["Y"].asc())

# Loading data from transactions collection in spark dataframe
dft = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri",
    "mongodb://127.0.0.1/test.transaction3").load()

class GetHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length'))

        # Extracting filters from request body
        post_body = self.rfile.read(content_len)
        filters = json.loads(post_body)["filters"]
        print filters

        # Lookup in product dataframe on the basis of filters given by user.
        # Select user_id column to increase join efficiency later
        dfp2 = dfp.where(dfp["Y"].isin(filters)).select(dfp["user_id"])

        # Unexpectedly dropDuplicates was slower. The reason probably is that there are not many duplicates.
        # dfp2 = dfp.where(dfp["Y"].isin(filters)).select(dfp["user_id"]).dropDuplicates(["user_id"])

        # Inner join of dft with dfp2 whre user_id is same
        # Taking out X & Z colums from joined dataframe
        dfr = dft.join(dfp2, dft["user_id"] == dfp2["user_id"]).select(dft["X"],dft["Z"])

        # Broadcast join was slower as dfp2 dataframe was large in size
        # dfr = dft.join(broadcast(dfp2), dft["user_id"] == dfp2["user_id"]).select(dft["X"],dft["Z"])

        # Using dataframe aggregration to find sum over column X
        sumVal = dfr.agg(F.sum("X")).head()[0]

        # Using dataframe aggregration to find average over column Y
        avgVal = dfr.agg(F.avg("Z")).head()[0]

        # Creating response & sending back
        response = {"sumX":sumVal,"avgZ":avgVal}
        print response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(response)
        return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', 8080), GetHandler)
    print 'Starting server at http://localhost:8080'
    server.serve_forever()
