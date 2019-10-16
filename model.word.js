const mongoose = require('mongoose');
const Schema = mongoose.Schema;

// schema holding information related to one project
let Word = new Schema({
    text: {
        type: String
    },
    count:{
    	type: Number
    },
    occurrences: {
    	//occurrences is list of objects like: [{"docid1":[100]},{"docid2":[1,5,300]}]
    	type: Array
    }
});


module.exports = mongoose.model('Word', Word);