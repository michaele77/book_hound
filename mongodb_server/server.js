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


// Create our mongoose connection
// Throw an error if fails to connect
mongoose.connect('mongodb://localhost/bookhound_proto_2') // Come back and check if this DB name is correct
mongoose.connection.once('open', function() {
    console.log('connected to boohound database!')
}).on('error', function(error) {
    console.log('Failed to connect! See error ~~  ' + error)
})


// --------------- Server API Functions below! --------------- //
// Note: We have no POST requests here! We have generated our database through webscraping already!


// READ A BOOK BY ID
// GET request
app.get('/fetch', function(req, res) {
    booksModel.find({}).then( function(DBitems) {
        res.send(DBitems) // Send whatever mongoose finds in the mongoDB
        console.log('Fetched book!')
    })
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