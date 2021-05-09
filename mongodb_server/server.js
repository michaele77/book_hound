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

    //  db = client.db('bookhound_proto_2')
     db = client.db('bookhound_mongodb_toMend') // This is the newly included image DB!
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



async function asyncFindFirstOrder(bookID) {

    let masterUserArr, masterUserRatingsArr
    let masterArr = []
    var dbItems = await booksColl.findOne({_id: bookID})
    // var dbItems = await query.exec()

    masterUserArr = dbItems.ratersID
    masterUserRatingsArr = dbItems.ratersRating


    // We have the user and raters IDs
    // We iterate through each user and get their books
    // Then concatenate the original user ID, their book ID, and the 2 ratings multiplied in an Array
    let curUsr, rating_usr2book, rating_book2usr, curBookArr, tmpRating
    for (let indx in masterUserArr) {
        // Iterate through masterUserArr and masterUserRatingsArr using indx as iterating var
        curUsr = masterUserArr[indx]
        rating_book2usr = masterUserRatingsArr[indx]
        curBookArr = []
        rating_usr2book = null


        dbItems = await userColl.findOne({_id: curUsr})
        // dbItems = await query.exec()

        curBookArr = dbItems.booksID
        rating_usr2book = dbItems.raterRatings

        // Now iterate through the array of books for each user
        // At each iteration in this inner loop, add to the 
        for (let bIndx in curBookArr) {
            tmpRating = rating_book2usr * rating_usr2book[bIndx]
            masterArr.push( [curUsr, curBookArr[bIndx], tmpRating] )
        }

    }
    return masterArr

}



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

// Create a triple list for every book-user pair which contains:
//     1) user ID
//     2) book ID
//     3) rating
// With these 3 things, the swift App can easily use its own user tables to calculate the true match score
app.get('/fetchFirstOrder', async function(req, res) {
    try {
        const queryObj = url.parse(req.url,true).query
        const bookID = Number(queryObj['bookID'])

        let bigArr = await asyncFindFirstOrder(bookID)
        console.log('we here mate')
        console.log(bigArr.length)
        res.send(bigArr)
        console.log('we after async!')

    } catch(err) {
        next(err)
    }

})





// Get all users in a list
// GET request
app.get('/fetchAllUserIDs', function(req, res) {
    try {
        // Have no arguments for this fetch, so no parsing needed
        // Return all of the documents in the user collection
        // Project the return to be only the user IDs
        const projectionArg = {"_id": 1}
        console.log("we here")
        userColl.find({})
        .toArray()
        .then( function(dbItems) {
            // Now need to prune out the ids only! Couldnt figure out a way to do it with Mongo queries
            console.log("we in")
            let idList = []
            for (let indx in dbItems) {
                idList.push(dbItems[indx]["_id"])
            }

            res.send({array: idList}) // Send whatever mongoose finds in the mongoDB
            console.log('Fetched all user IDs! There were ' + String(idList.length) + ' users returned!')
        })
    } catch(err) {
        next(err)
    }

})


// Get all books in a list
// GET request
app.get('/fetchAllBookIDs', function(req, res) {
    try {
        // Have no arguments for this fetch, so no parsing needed
        // Return all of the documents in the user collection
        // Project the return to be only the user IDs
        const projectionArg = {"_id": 1}
        console.log("we here")
        booksColl.find({})
        .toArray()
        .then( function(dbItems) {
            // Now need to prune out the ids only! Couldnt figure out a way to do it with Mongo queries
            console.log("we in")
            let idList = []
            for (let indx in dbItems) {
                idList.push(dbItems[indx]["_id"])
            }

            res.send({array: idList}) // Send whatever mongoose finds in the mongoDB
            console.log('Fetched all book IDs! There were ' + String(idList.length) + ' books returned!')
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