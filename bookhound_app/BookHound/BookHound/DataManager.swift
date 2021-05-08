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
    var userIDs: [Int] = []
    var matchScoreDict: [Int: Float] = [:]
    var sortedMatchKeys: [Int] = []
    
    let server = serverLink()
     
    
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
    // This should be called everytime we want to retrieve the top book
    func sortMatchKeys() {
        // 1-liner to sort by values and return the keys
        self.sortedMatchKeys = Array(self.matchScoreDict.keys).sorted(by: {self.matchScoreDict[$0]! > self.matchScoreDict[$1]!})
        let topKey = self.sortedMatchKeys[0]
                
        print("Top key is \(topKey) with value of \(self.matchScoreDict[topKey])")
    }
    
    
    // Function to update match score dictionary with preffered initialized favorite book
    // Singular version of similar functin below
    func updateFavoriteMatch(book: Int) {
        // We are given an array of book IDs representing favorite books
        // For each book, we want to update all match scores of linked users that like this book
        
        let favUpdateVal: Float = 5.0 // Pretty high increment value! fiddle with this to change starting state
        print("IN UPDATE FUNC: updating \(book)")
        
        self.server.fetchBook_byID(bookID: book) { (bookData) in
            // Closure code
            // We want to update matchScore Dictionary AFTER server comms stop
            var seenSet = Set<Int>()
            for curUser in self.server.cachedBook.ratersID {
                if (self.matchScoreDict[curUser] != nil) {
                    if (seenSet.contains(curUser)) {
                        print(" ~We have seen a repeat (on user \(curUser))")
                    } else {
                        self.matchScoreDict[curUser]! += favUpdateVal
                        seenSet.insert(curUser)
                    }
                
                    
                } else {
                    print("ERROR- could not find user ID in the dictionary, this should not happen...")
                }
     
            }
            print("Done with dispatched queue execute!")
            
        }
        

        
//        self.server.fetchBook_byID(bookID: book)
//
//        // Dispatch a delayed, timed functin execution
//        // Any dependency on server data needs to be done with delayed execution
//        DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
//
//            // FOUND A BUG IN DATABASE
//            // Apparently...we have duplicate users connected to books, must have not pruned these during consolidation...
//            // Solution: Keep a hashset of seen users, refuse to add them if they appear in the hashset
//            // Not ideal..but better than rerunning database consolidation
//            var seenSet = Set<Int>()
//            for curUser in self.server.cachedBook.ratersID {
//                if (self.matchScoreDict[curUser] != nil) {
//                    if (seenSet.contains(curUser)) {
//                        print(" ~We have seen a repeat (on user \(curUser))")
//                    } else {
//                        self.matchScoreDict[curUser]! += favUpdateVal
//                        seenSet.insert(curUser)
//                    }
//
//
//                } else {
//                    print("ERROR- could not find user ID in the dictionary, this should not happen...")
//                }
//
//            }
//            print("Done with dispatched queue execute!")
//        }
        
        print("Done with updating favorite match (dispatched thread still running)")
        
    }
    
        
    
    // Function to update match score dictionary with preffered initialized favorite books
    // We can tweak how much weight we want to give to our favorite books here
    func updateFavoriteMatches(bookList: [Int]) {
        // We are given an array of book IDs representing favorite books
        // For each book, we want to update all match scores of linked users that like this book
        
        let favUpdateVal: Float = 5.0 // Pretty high increment value! fiddle with this to change starting state
        print("IN UPDATE FUNC: updating \(bookList)")
        
        for curBook in bookList {
            self.server.fetchBook_byID(bookID: curBook) { (bookData) in
                // Closure completion code
                for curUser in self.server.cachedBook.ratersID {
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
