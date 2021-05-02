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
    static let sharedInstance = DataManager()
    
    var testString: String = ""
}
