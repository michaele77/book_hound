//
//  ParamConfig.swift
//  BookHound
//
//  Created by Michael Ershov on 5/23/21.
//

import Foundation

// We will define all of our algorithm-related parameters here
// Will be easy to collect all of the tweaks in one place for future expirementation


struct ParamConfig {
    // Initial book-selector weights
    static let initSelWeight: Float = 20.0
    
    // Cardinal swipe weights
    static let read_bad: Float      = -2.0
    static let read_good: Float     = 2.0
    static let notread_bad: Float   = -1.0
    static let notread_good: Float  = 1.0
}



