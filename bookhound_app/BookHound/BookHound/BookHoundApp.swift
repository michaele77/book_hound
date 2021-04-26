//
//  BookHoundApp.swift
//  BookHound
//
//  Created by Michael Ershov on 4/10/21.
//

import SwiftUI


//protocol DataDelegate {
//    func updateBookView(newArr: String)
//}


@main
struct BookHoundApp: App {
    var body: some Scene {
        
        WindowGroup {
            initialSelectionView()
        }
    }
}
