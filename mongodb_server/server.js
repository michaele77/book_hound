const express = require('express')
var app = express()
const url = require('url')

// Import the models defined in bookhoundSchema 
// Have 2 schema types so need to import both of them
var modelVars = require('./bookhoundSchema') 
var booksModel = modelVars.booksModel
var usersModel = modelVars.usersModel

// Import secret personal IP address so it's not exposed on github
const mySecretIP = require('./personal_IP')


var MongoClient = require('mongodb').MongoClient
// Define global variables
var booksColl, userColl, db

// Connect to the db
MongoClient.connect("mongodb://localhost", function (err, client) {
   
     if(err) throw err;

     db = client.db('bookhound_proto_2')
     console.log('connected to boohound database!')

     booksColl = db.collection('books')
     userColl = db.collection('users')


     //Write databse Insert/Update/Query code here..
     
                
});








// --------------- Server API Functions below! --------------- //
// Note: We have no POST requests here! We have generated our database through webscraping already!



// READ A BOOK BY ID
// GET request
// URL must be of ID type: bookID = x, where x is required book ID
app.get('/fetchBook', function(req, res) {
    // const urlArr = req.url.split('?')
    // const singleArg = urlArr[urlArr.length - 1]

    try {
        const queryObj = url.parse(req.url,true).query
        const bookID = Number(queryObj['bookID'])
        booksColl.findOne({_id: bookID}).then( function(dbItems) {
            res.send(dbItems) // Send whatever mongoose finds in the mongoDB
            console.log('Fetched book ' + String(bookID) + '!')
        })
    } catch(err) {
        next(err)
    }

    
})



// READ A USER BY ID
// GET request
// URL must be of ID type: userID = x, where x is required user ID
app.get('/fetchUser', function(req, res) {
    try {
        const queryObj = url.parse(req.url,true).query
        const userID = Number(queryObj['userID'])
        userColl.findOne({_id: userID}).then( function(dbItems) {
            res.send(dbItems) // Send whatever mongoose finds in the mongoDB
            console.log('Fetched user ' + String(userID) + '!')
        })
    } catch(err) {
        next(err)
    }

})





// GENERATE FIRST-ORDER BOOKS LIST 
// GET request

// Note! Here, we are NOT ordering the books by matches, we will be doing that at the client level
// This is because the client has their own custom mapping of users to matchScore
// Therefore, returning the most-hits first order book match would be innapropriate 

// In the worst case, we will have ~8460 users linked to HP #1 and 156 books linked by a single user
// In average, books have 7.48 users and users have 105.75 books
// So we can expect to return:
//      -On average     ~791 book IDs       --> ~6kB of data
//      -In worst case  ~894,645 book IDs   --> ~7MB of data

app.get('/fetchFirstOrder', function(req, res) {
    try {
        const queryObj = url.parse(req.url,true).query
        const userID = Number(queryObj['userID'])
        userColl.findOne({_id: userID}).then( function(dbItems) {
            res.send(dbItems) // Send whatever mongoose finds in the mongoDB
            console.log('Fetched user yikes!')
        })
    } catch(err) {
        next(err)
    }

})





app.use((req, res, next) => {
    const error = new Error("Not found");
    error.status = 404;
    next(error);
    console.log('Requested routine not found, sent 404')
  });
  
  // error handler middleware
  app.use((error, req, res, next) => {
    console.log('Middleware error handler entree')
      res.status(error.status || 500).send({
        error: {
          status: error.status || 500,
          message: error.message || 'Internal Server Error',
        },
      });
    });



// Exclude the IP to allow external IPs from outside the network
var server = app.listen(8084, mySecretIP, function() {
    console.log('Server is up and running!')
})