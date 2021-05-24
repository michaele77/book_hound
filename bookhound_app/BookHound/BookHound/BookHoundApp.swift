//
//  BookHoundApp.swift
//  BookHound
//
//  Created by Michael Ershov on 4/10/21.
//

import SwiftUI


@main
struct BookHoundApp: App {
    // At startup, lets load the userlist
    
    
    var body: some Scene {
        
        WindowGroup {
            OpenAppView()
//            initialSelectionView()
        }
    }
}
