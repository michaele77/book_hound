var mongoose = require('mongoose')
var Schema = mongoose.Schema


// Define our schemas for books and users 
// Match all naming conventins with in our python generation script as well as in swift App
var BookSchema = new Schema( {

    _id: Number,
    title: String,
    href: String,
    author: String,
    meta: String,
    details: String,
    series: String,
    summary: String,
    imageSource: String,
    imageBinary: String,
    fullParameter: Boolean,
    ratersID: [Number],
    ratersRating: [Number]

})

var UserSchema = new Schema( {

    _id: Number,
    name: String,
    link: String,
    ratingsLink: String,
    booksID: [Number],
    ratersRating: [Number]

})

// Create models of our schemas
const booksModel = mongoose.model('booksModel', BookSchema)
const usersModel = mongoose.model('usersModel', UserSchema)

// Make models available to our server.js file
module.exports = {
    booksModel,
    usersModel
}