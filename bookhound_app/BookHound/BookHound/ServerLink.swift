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


struct genreObject: Decodable {
    var genreLabelList: [String]
    var normalizedWeight: Float
}


struct IDList: Decodable {
    var array: [Int]
}


struct nearestNeighbor: Decodable {
    var array: [nearestTriplet]

    
struct nearestTriplet: Decodable {
    var userID: Int
    var bookID: Int
    var rating: Float // TODO: Check this! I think there are some 4.5's in there...
}



class serverLink {
    
    var cachedBook = Book()
    var cachedUserIDs: Set<Int> = []
    var cachedBookIDs: Set<Int> = []
    
    init() {
       print("initializing serverLink class~~")
    }
    
    
    func fetchBook_byID(bookID: Int, completion: @escaping (Book) -> Void) {
        
        // Books to fetch:
        // kingkiller chronicles: 186074
        // 3 body problem: 20518872
        // HP 1: 3
        // LOTR: 119
        // Gun slinger: 43615
        
        AF.request("http://192.168.1.72:8084/fetchBook?bookID=" + String(bookID)).responseJSON {
            response in
            print(response.data)
            let data = String(data: response.data!, encoding: .utf8)
//            print(data!)
                        
            do {
                let decoder = JSONDecoder()
//                decoder.dateDecodingStrategy = .iso8601

                self.cachedBook = try decoder.decode(Book.self, from: (data?.data(using: .utf8))!)
                print("JSON unpacking successful! See prints below...")
                
                // Pass data to closure
                completion(self.cachedBook)
                            
            } catch {
                self.cachedBook = Book() // Reinitialize to inform that data failed
                print("Could not unwrap the JSON! See error:")
                print(error) // error is a local variable in any do/catch block!
                
                // Pass data to closure
                completion(self.cachedBook)
                
            }
            
        }
        
    }
    
    
    func fetchUsers_allIDs(completion: @escaping ([Int]) -> Void) {
        AF.request("http://192.168.1.72:8084/fetchAllUserIDs").responseJSON {
            response in
            
            let data = String(data: response.data!, encoding: .utf8)
            
            do {
                let decoder = JSONDecoder()
//                decoder.dateDecodingStrategy = .iso8601

                let tempArr = try decoder.decode(IDList.self, from: (data?.data(using: .utf8))!)
                self.cachedUserIDs = Set(tempArr.array)
                print("JSON unpacking successful! See prints below...")
                completion(tempArr.array)
                            
            } catch {
                print("Could not unwrap the JSON! See error:")
                print(error) // error is a local variable in any do/catch block!
                completion([])
                
            }
            
        }
        
    }
    
    
    
    func fetchBooks_allIDs(completion: @escaping ([Int]) -> Void) {
        AF.request("http://192.168.1.72:8084/fetchAllBookIDs").responseJSON {
            response in
            
            let data = String(data: response.data!, encoding: .utf8)
            
            do {
                let decoder = JSONDecoder()

                let tempArr = try decoder.decode(IDList.self, from: (data?.data(using: .utf8))!)
                self.cachedBookIDs = Set(tempArr.array)
                print("JSON unpacking successful! See prints below...")
                completion(tempArr.array)
                            
            } catch {
                print("Could not unwrap the JSON! See error:")
                print(error) // error is a local variable in any do/catch block!
                completion([])
                
            }
            
        }
    }
    
    
    func fetchFirstOrder(bookID: Int, completion: @escaping ([nearestTriplet]) -> Void) {
        AF.request("http://192.168.1.72:8084/fetchFirstOrder?bookID=" + String(bookID)).responseJSON {
            response in
            
            let data = String(data: response.data!, encoding: .utf8)
            
            do {
                let decoder = JSONDecoder()

                let tempArr = try decoder.decode(nearestNeighbor.self, from: (data?.data(using: .utf8))!)
                print("JSON unpacking successful! See prints below...")
                completion(tempArr.array)
                            
            } catch {
                print("Could not unwrap the JSON! See error:")
                print(error) // error is a local variable in any do/catch block!
                completion([])
                
            }
            
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
