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
    let server = serverLink()
    
    // Function to initialize the match score dictionary
    // This should be run only once
    func initializeMatchScores() {
        if (matchScoreDict.isEmpty && userIDs.count > 0) {
            // If we are here, then our matchscore has not been initialized
            for curID in userIDs {
                matchScoreDict[curID] = 1.0
            }
            
        } else {
            // Print correct error
            print("ERROR- match score initialization rejected! See below for prognosis:")
            
            if (matchScoreDict.isEmpty) {
                print("userIDs have not been fetched")
            } else if (userIDs.count > 0) {
                print("match scores have already been initialized ")
            } else {
                print("BOTH userIDs have not been fetched AND match scores have already been initialized...")
            }
        }
    }
    
    // Function to update match score dictionary with preffered initialized favorite books
    // We can tweak how much weight we want to give to our favorite books here
    func updateFavoriteMatches(bookList: [Int]) {
        // We are given an array of book IDs representing favorite books
        // For each book, we want to update all match scores of linked users that like this book
        
        
    }
}
