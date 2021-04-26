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
}

// TODO: uncomment below
////  Main serverLink class to talk with nodeJS server
class ServerLink {
    
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
            
            let dataJSON = JSONDecoder.decode([Book].self, from: data)
            
            print(data!)
            print("----PARTITION---")
            print(data.author)
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
