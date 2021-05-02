//
//  ServerLink.swift
//  BookHound
//
//  This file is responsible for talking with node JS server and recieving book data
//
//  Created by Michael Ershov on 4/24/21.
//


import Foundation
import Alamofire


//  Need to define what a user and book looks like
//  Define as 2 structs

struct User: Decodable {
    var _id: Int
    var name: String
    var link: String
    var ratingsLink: String
    var booksID: [Int]
    var raterRatings: [Float]
}

struct Book: Decodable {
    var _id: Int
    var title: String
    var href: String
    var author: String
    var meta: String
    var details: String
    var series: String
    var summary: String
    var imageSource: String
    var imageBinary: String // TODO: Figure out how to store an image binary in swift!
    var fullParameter: Bool
    var ratersID: [Int]
    var ratersRating: [Float]
    var genres: [genreObject]
    var genreWeight: Int
    var dateUpdated: String
    init() {
        self._id = -1
        self.title = "INIT"
        self.href = "INIT"
        self.author = "INIT"
        self.meta = "INIT"
        self.details = "INIT"
        self.series = "INIT"
        self.summary = "INIT"
        self.imageSource = "INIT"
        self.imageBinary = "INIT"
        self.fullParameter = false
        self.ratersID = []
        self.ratersRating = []
        self.genres = []
        self.genreWeight = -1
        self.dateUpdated = "INIT"
    }
}

//struct Book: Decodable {
//    var _id: Int?
//    var title: String?
//    var href: String?
//    var author: String?
//    var meta: String?
//    var details: String?
//    var series: String?
//    var summary: String?
//    var imageSource: String?
//    var imageBinary: String? // TODO: Figure out how to store an image binary in swift!
//    var fullParameter: Bool?
//    var ratersID: [Int]?
//    var ratersRating: [Float]?
//    var genres: [genreObject]?
//    var genreWeight: Int?
//    var dateUpdated: String?
//}

struct genreObject: Decodable {
    var genreLabelList: [String]
    var normalizedWeight: Float
}

// TODO: uncomment below
////  Main serverLink class to talk with nodeJS server
class serverLink {
    
    var cachedBook = Book()
    
    init() {
       print("initializing serverLink class~~")
    }
    
    
    func fetchBook_byID(bookID: Int) {
        
        AF.request("http://192.168.1.72:8084/fetchBook?bookID=186074").responseJSON {
            response in
            print(response.data)
            let data = String(data: response.data!, encoding: .utf8)
//            print(data!)
                        
            do {
                let decoder = JSONDecoder()
//                decoder.dateDecodingStrategy = .iso8601

                self.cachedBook = try decoder.decode(Book.self, from: (data?.data(using: .utf8))!)
                print("JSON unpacking successful! See prints below...")
                            
            } catch {
                self.cachedBook = Book() // Reinitialize to inform that data failed
                print("Could not unwrap the JSON! See error:")
                print(error) // error is a local variable in any do/catch block!
                
            }
            
        }
                
    }


//    //  Fetch function: Get user JSON by user ID
//    func fetchUser_byID {
//
//
//    }
//
//    //  Fetch function: get user JSON by user name
//    func fetchUser_byName {
//
//    }


}
