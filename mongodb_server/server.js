const express = require('express')
const mongoose = require('mongoose')
var app = express()

// Import the models defined in bookhoundSchema 
// Have 2 schema types so need to import both of them
var modelVars = require('./bookhoundSchema') 
var booksModel = modelVars.booksModel
var usersModel = modelVars.usersModel

// Import secret personal IP address so it's not exposed on github
const mySecretIP = require('./personal_IP')


// // Create our mongoose connection
// // Throw an error if fails to connect
// mongoose.connect('mongodb://localhost:27017/bookhound_proto_2') // Come back and check if this DB name is correct
// mongoose.connection.once('open', function() {
//     console.log('connected to boohound database!')
// }).on('error', function(error) {
//     console.log('Failed to connect! See error ~~  ' + error)
// })


// var action = function (err, collection) {
//     // Locate all the entries using find
//     collection.find({'_id':'b'}).toArray(function(err, results) {
//         /* whatever you want to do with the results in node such as the following
//              res.render('home', {
//                  'title': 'MyTitle',
//                  'data': results
//              });
//         */
//     });
// };

// mongoose.connection.db.collection('question', action);



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
app.get('/fetch', function(req, res) {
    booksColl.findOne({_id: 3}).then( function(dbItems) {
        res.send(dbItems) // Send whatever mongoose finds in the mongoDB
        console.log('Fetched book!')
    })



// READ A USER BY ID
// GET request



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



var server = app.listen(8081, mySecretIP, function() {
    console.log('Server is up and running!')
})