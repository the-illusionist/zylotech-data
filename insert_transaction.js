var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');

var url = 'mongodb://localhost:27017/test';

MongoClient.connect(url, function(err, db) {
	assert.equal(null, err);
	console.log("Connected correctly to server.");
	// var bulk = db.collection('product').initializeUnorderedBulkOp();  //Bulk & insertMany both have smae implementation internally
	var totalRecords = 1000000;
	var arr = []
	var i=0;
	while(i<totalRecords){
		uId = Math.random().toString().slice(2,12);
		xVal = Math.random().toString().slice(2,7);
		zVal = Math.random().toString().slice(2,8);
		record = {"user_id":uId, "X":xVal , "Z":zVal};
		// bulk.insert(record);
		arr.push(record);
		i++;
		if(i%100000 == 0)
			console.log(i + " inserted");
	}
	// bulk.execute();
	db.collection('transaction3').insertMany( arr ,{ordered:false})
	// db.close();
});
