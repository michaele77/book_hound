//
//  DataManager.swift
//  BookHound
//
//  Created by Michael Ershov on 5/1/21.
//

// This file is a global data class that will be initialized at launch and used to store the data to share between all views
// We will declare everything in here as static so it is available by default

import Foundation


class DataManager {
    // Create static, global instance that can be passed around between views
    // This is technically a "global" class/variable, but better than passing around bits and pieces of data and here I think
    static let sharedInstance = DataManager()
    
    var testString: String = ""
    var userIDs: Set<Int> = []
    var bookIDs: Set<Int> = []
    var matchScoreDict: [Int: Float] = [:]
    var sortedMatchKeys: [Int] = []
    var bookScoreDict: [Int: Float] = [:]
    var sortedBookKeys: [Int] = []
    
    // This is the set of all books we've seen
    // Use this to make sure we dont re-recommend books
    var encounteredBooks: Set<Int> = []
    let server = serverLink()
    var cachedBook = Book()
     
    
    // Function to initialize the match score dictionary
    // This should be run only once
    func initializeMatchScores() {
        if (self.matchScoreDict.isEmpty && self.userIDs.count > 0) {
            // If we are here, then our matchscore has not been initialized
            for curID in self.userIDs {
                self.matchScoreDict[curID] = 1.0
            }
            print("Finished matchScoreDict setup!")
            
        } else {
            // Print correct error
            print("ERROR- match score initialization rejected! See below for prognosis:")
            
            if (self.matchScoreDict.isEmpty) {
                print("userIDs have not been fetched")
            } else if (self.userIDs.count > 0) {
                print("match scores have already been initialized ")
            } else {
                print("BOTH userIDs have not been fetched AND match scores have already been initialized...")
            }
        }
    }
    
    // Helper function to update the matchScore dictionary sort
    // Sort the helper dictionary by value and output the keys into the shared instance variable
    // This should be called everytime we want to retrieve the top User
    func sortMatchKeys() {
        // 1-liner to sort by values and return the keys
        self.sortedMatchKeys = Array(self.matchScoreDict.keys).sorted(by: {self.matchScoreDict[$0]! > self.matchScoreDict[$1]!})
        let topKey = self.sortedMatchKeys[0]
        
        // Get some more debug prints for testing...
        // Test top key
        print("Top key is \(topKey) with value of \(self.matchScoreDict[topKey]!)")
        // Test getting a counter of key/value frequencies
        let countArray = matchScoreDict.values.map { ($0, 1) } // Map all of the dictionary values to a key value pair with each equaling 1
        let valueFrequency = Dictionary(countArray, uniquingKeysWith: +) // Create dictionary from count array, adding when collision occures with hasing counts
        print(valueFrequency)
        // Test getting the top and bottom occurance freuquency values
        let vfVals = valueFrequency.keys
        let minValCnt = valueFrequency[vfVals.max()!]
        let maxValCnt = valueFrequency[vfVals.min() ?? 1.0]
        print("we have \(minValCnt!) gods and \(maxValCnt!) shitters")
    }
    
    
    // Very simple helper function to reduce verbosity
    func grabBookScore(index: Int) -> Float {
        return self.bookScoreDict[ self.sortedBookKeys[index] ] ?? 0
    }
    
    // Simple helper to pop the sorted book keys list any encountered IDs
    func removeEncountered() {
        while true {
            if self.encounteredBooks.contains(self.sortedBookKeys.last ?? -1) {
                let tmpVar = self.sortedBookKeys.popLast()
                print("     //\\ Popped book ID \(tmpVar)")
            } else {
                break
            }
        }
    }
    
    // Helper function to update the bookScore dictionary sort
    // Sort the helper dictionary by value and output the keys into the shared instance variable
    // This should be called everytime we want to retrieve the top book
    // In this function, make sure to delete any books we've seen already
    func sortBookKeys(completion: @escaping (Book) -> Void) {
        // 1-liner to sort by values and return the keys
        self.sortedBookKeys = Array(self.bookScoreDict.keys).sorted(by: {self.bookScoreDict[$0]! < self.bookScoreDict[$1]!})
        removeEncountered()
        let topKey = self.sortedBookKeys.last ?? -1
        let endIndx = self.sortedBookKeys.count-1
        
        
        // Get some more debug prints for testing...
        // Test top key
        print("Top key is \(topKey) with value of \(self.bookScoreDict[topKey]!)")
        
        // Grab just the topkey
        self.server.fetchBook_byID(bookID: topKey) {topBook in
            self.cachedBook = topBook
            print("Done getting the topBook!")
            completion(self.cachedBook)
        }
        
        // We can print other useful stuff from the top key
        print("See the top books below:")
        for i in 0...5 {
            let thisBookId = self.sortedBookKeys[endIndx-i]
            self.server.fetchBook_byID(bookID: thisBookId) { bookData in
                print("  ~index \(endIndx-i) --> book ID is \(thisBookId), with name \(bookData.title) with score of \(self.grabBookScore(index: endIndx-i))")
            }
            
        }
        
        
        print("~~~~~~DONE with Data manager sort!")
        
//        DispatchQueue.main.async {
//            self.SwipeEngineView.imgString = "Data manager done w sort!"
//        }
        
        // Below is code to map the frequency of the book score occurances
        // This makes sense to do with match scores in users (very samll number of potential match scores), not so much with all possible book scores...
//        let countArray = bookScoreDict.values.map { ($0, 1) } // Map all of the dictionary values to a key value pair with each equaling 1
//        let valueFrequency = Dictionary(countArray, uniquingKeysWith: +) // Create dictionary from count array, adding when collision occures with hasing counts
//        print(valueFrequency)
//        // Test getting the top and bottom occurance freuquency values
//        let vfVals = valueFrequency.keys
//        let minValCnt = valueFrequency[vfVals.max()!]
//        let maxValCnt = valueFrequency[vfVals.min() ?? 1.0]
//        print("we have \(minValCnt!) god-like books and \(maxValCnt!) shitter-like books")
    }
    
    
    
    
    // Helper function to initialize the book score dictionary
    // This should only be run once!
    func initializeBookScores() {
        if (self.bookScoreDict.isEmpty && self.bookIDs.count > 0) {
            // If we are here, then our matchscore has not been initialized
            for curID in self.bookIDs {
//                if curID == 22628 {
//                    print("Saw this NUMBERRRRRR")
//                    self.server.fetchBook_byID(bookID: curID) { (thisBook) in
//                        print("Full param is \(thisBook.fullParameter)")
//                    }
//                }
                self.bookScoreDict[curID] = 1.0
            }
            print("Finished bookScoreDict setup!")
            
        } else {
            // Print correct error
            print("ERROR- match score initialization rejected! See below for prognosis:")
            
            if (self.bookScoreDict.isEmpty) {
                print("bookIDs have not been fetched")
            } else if (self.bookIDs.count > 0) {
                print("book scores have already been initialized ")
            } else {
                print("BOTH bookIDs have not been fetched AND book scores have already been initialized...")
            }
        }
    }
    
    
    
    
    // Helper function to sort a list of books in the descending order, so that caching top X books is easy
    // TODO: we actually dont need to sort the entire book list, we can simply grab the top X books == O(N) instead of O(NlogN)
    // The sorting value will be determined by: matchScore * user_bookA * user_bookB
    // TODO: PUT THE FUNCTION IN!!
    
    
    
    
    
    
    // Function to update match score dictionary with preffered initialized favorite book
    // Singular version of similar functin below
    // MODIFICATION: add add value as input; that way we can reuse this function both for favorite book initialization as well as in the swipe engine
    
    // NOTE: after we update our match scores, we also want to get the nearest neigbor books of the current book
    // THEN, use the updated match scores and users to update all of the book scores in our bookScore dictionary
    // Need to do this here to avoid data race conditions in the view files
    func updateFavoriteMatch(book: Int, updateWeight: Float) {
        // We are given an array of book IDs representing favorite books
        // For each book, we want to update all match scores of linked users that like this book
        self.encounteredBooks.insert(book) // Update our encountered books set
        
        self.server.fetchBook_byID(bookID: book) { (bookData) in
            // Closure code
            // We want to update matchScore Dictionary AFTER server comms stop
            if bookData.ratersID.isEmpty {
                // Here if the book has not been completely scraped
                print("Input an incomplete book, cannot update match score dictionary!!")
                return
            }
            
            var seenSet = Set<Int>()
            for (indx, curUser) in bookData.ratersID.enumerated() {
                
                // Check if matchScoreDict has a key corresponding to curUser AND assign that key's value to curVal
                if let curVal = self.matchScoreDict[curUser] {
                    if (seenSet.contains(curUser)) {
                        print(" ~We have seen a repeat (on user \(curUser))")
                    } else {
                        self.matchScoreDict[curUser] = curVal + updateWeight
                        seenSet.insert(curUser)
                    }
                    
                } else {
                    // If here, return from function (dont continue)
                    print("ERROR- could not find user ID in the dictionary, this should not happen...")
                    return
                }
                
            }

            // Done updating the matchscore dictionary
            // Now execute search nearest neigbor query on our server
            self.server.fetchFirstOrder(bookID: book) { (tripletArr) in
                // This tripletArr contains:
                // 1) User ID
                // 2) Book ID
                // 3) rating that links them
                
                
                // We have pre-computed on the server the bookA -> user -> book B chain
                // So now all we need to do is multiply this by that user's match score
                // At the end of this, we will have a max score of MS*25, add this to bookscore
                
                // By the structure of the JSON, the user IDs are in order; so the same user will continue until all of their books are done in order
                var tmpTicker = 0
                for curNeighbor in tripletArr {
                    let curMatchScore = self.matchScoreDict[curNeighbor.userID]!
                    let finalScore = curMatchScore * curNeighbor.rating
                    if let prevBookScore = self.bookScoreDict[curNeighbor.bookID] {
                        // Here if the dictionary entree exists
                        self.bookScoreDict[curNeighbor.bookID] = prevBookScore + finalScore
                        
                    } else {
                        // We are here because the consolidation script was not foolproof
                        // The "duplicates" of especially popular books have not neccessarily been deleted
                        // Affects < 0.5% of all books, so not really an issue yet...might need to revisit though
                        // Example: Perks of being a Wallflower: shows 44451907, real one is 22628 that is in the DB
                        print("Uh oh...\(curNeighbor.bookID) doesnt exist in the dictionary!")
                        tmpTicker += 1
                    }
                }
                
                print("Total number of detatched books is \(tmpTicker)")
                
                
                
                
                print("TODO HERE")
                
            }
            
            
            // End of closure ~~
        }
        
                
    }
    
    

    
        
    
    // Function to update match score dictionary with preffered initialized favorite books
    // We can tweak how much weight we want to give to our favorite books here
    func updateFavoriteMatches(bookList: [Int]) {
        // We are given an array of book IDs representing favorite books
        // For each book, we want to update all match scores of linked users that like this book
        
//        let favUpdateVal: Float = 5.0 // Pretty high increment value! fiddle with this to change starting state
        
        let favUpdateVal = ParamConfig.initSelWeight
        
        print("IN UPDATE FUNC: updating \(bookList)")
        
        for curBook in bookList {
            self.server.fetchBook_byID(bookID: curBook) { (bookData) in
                // Closure completion code
                for curUser in bookData.ratersID {
                    if (self.matchScoreDict[curUser] != nil) {
                        self.matchScoreDict[curUser]! += favUpdateVal
                        print("---updated user \(curUser) to \(self.matchScoreDict[curUser])")
                    } else {
                        print("ERROR- could not find user ID in the dictionary, this should not happen...")
                    }
                    
                }
            }
                
        }
    }
            
            
}
