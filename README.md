# zylotech-data

Project is intended to execute a filter & aggregation on large datasets stored in two different mongo collection related by a common key using Apache Spark. 

### Prerequisites:
* MongoDB (3.4+)
* Python (2.6+)
* Java (JDK6+)
* Apache Spark (1.6+)
* NodeJs (6.0+)
* Npm (3.6+)
* spark-mongo connector (2.0+)

### Steps to run:

1. sudo service mongod start (For Ubuntu) or brew services start mongodb (For Mac)
2. cd "source_directory"
3. npm install
4. node insert.js
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

### Summary:
We first insert the data into MongoDB using nodejs & node-mongoclient. Then we create a python server which is ready to listen at port 8080 for incoming filter request & also loads data from both collections in two spark dataframes using spark-mongo connector. User hits the server with required filters as a json object using which we apply filter operations on first dataframe & join it with second dataframe based on common key. Then we perform aggregation operations like sum & avg on columns of this joined dataframe. After calculation these, we reply to user with the desired values as a json object.


