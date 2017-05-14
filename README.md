# zylotech-data

Project is intended to execute a filter & aggregation on datasets stored in two different mongo collection related by a common key using spark.

### Prerequisites:
* MongoDB (3.4+)
* Python (2.6+)
* Java (JDK6+)
* Apache Spark (1.6+)
* NodeJs (6.0+)
* Npm (3.6+)
* spark-mongo connector (2.0+)

### Steps to run:

1. sudo service mongod start (For Ubuntu) or brew services start mongodb
2. cd "source_directory"
3. npm install
4. node insert_product.js
5. node insert_transaction.js
6. "spark_directory"/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.0.0 main.py

Once server is listening for requests:

curl -X POST \
  http://localhost:8080/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
	"filters":["a","c"]
}'

Sample response:

{'avgZ': 520511.71428571426, 'sumX': 2342383.0}


