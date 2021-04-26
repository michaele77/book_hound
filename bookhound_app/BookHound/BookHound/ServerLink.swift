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
//    var genres: [genreObject]
    var dateUpdated: Date
}
//
//extension Book {
//    init(from decoder: Decoder) throws {
//        let container = try decoder.container(keyedBy: CodingKeys.self)
//
//        let _id = try container.decode(String.self, forKey: ._id)
//        let title = try container.decode(String.self, forKey: .title)
//        let href = try container.decode(String.self, forKey: .href)
//        let author = try container.decode(String.self, forKey: .author)
//        let meta = try container.decode(String.self, forKey: .meta)
//        let details = try container.decode(String.self, forKey: .details)
//        let series = try container.decode(String.self, forKey: .series)
//        let summary = try container.decode(String.self, forKey: .summary)
//        let imageSource = try container.decode(String.self, forKey: .imageSource)
//        let imageBinary = try container.decode(String.self, forKey: .imageBinary)
//        let fullParameter = try container.decode(String.self, forKey: .fullParameter)
//        let ratersID = try container.decode(String.self, forKey: .ratersID)
//        let ratersRating = try container.decode(String.self, forKey: .ratersRating)
//        let genres = try container.decode(String.self, forKey: .genres)
//        let dateUpaded = try container.decode(String.self, forKey: .dateUpaded)
//    }
//
//    enum CodingKeys: String, CodingKey {
//        case _id = "_id"
//        case title = "title"
//        case href = "href"
//        case author = "author"
//        case meta = "meta"
//        case details = "details"
//        case series = "series"
//        case summary = "summmary"
//        case imageSource = "imageSource"
//        case imageBinary = "imageBinary"
//        case fullParameter = "fullParameter"
//        case ratersID = "ratersID"
//        case ratersRating = "ratersRating"
//        case genres = "genres"
//        case dateUpaded = "dateUpdated"
//    }
//}

struct genreObject: Decodable {
    var genreArr: [String]
    var votingCount: Int
}

// TODO: uncomment below
////  Main serverLink class to talk with nodeJS server
class serverLink {
    
    init() {
       print("initializing serverLink class~~")
    }
    
//    static let functions = ServerLink()
    
    func viewDidLoad() {
        print("I am in the class!")
        
        AF.request("http://192.168.1.72:8084/fetchBook?bookID=186074").responseJSON {
            response in
            print(response.data)
            let data = String(data: response.data!, encoding: .utf8)
            
            print(data!)
            print("----PARTITION---")
                        
            
//            var dataJSON: Book
            
            do {
                let decoder = JSONDecoder()
                decoder.dateDecodingStrategy = .formatted(DateFormatter.iso8601)
                var dataJSON = try decoder.decode(Book.self, from: (data?.data(using: .utf8))!)
                print("JSON unpacking successful! See prints below...")
                print(dataJSON.dateUpdated)
            } catch {
                print("Could not unwrap the JSON! See This error!!")
                print(error) // error is a local variable in any do/catch block!
            }
            
            
            
            
            
//            print(data.author)
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
