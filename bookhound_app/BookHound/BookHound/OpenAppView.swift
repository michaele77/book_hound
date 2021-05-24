//
//  OpenAppView.swift
//  BookHound
//
//  Created by Michael Ershov on 5/23/21.
//

import SwiftUI

struct OpenAppView: View {
    
    let server = serverLink()
    @State var doneWithLoading = false
    
    var body: some View {
        NavigationView {
            VStack {
                Text("Loading...")
                NavigationLink(destination: initialSelectionView(), isActive: $doneWithLoading){ EmptyView() }.hidden()
            }
        }.onAppear(perform: buildLists)
    }
    
    func buildLists() {
        // Load in all of the userIDs
        // Initialize userID match scores and user IDs in shared instane of DM
        self.server.fetchUsers_allIDs() {(userList) in
            // Completon closure code:
            // Execute based on closure to ensure that data is available after server query
            print("number of Ids we have \(userList.count)")
            DataManager.sharedInstance.userIDs = server.cachedUserIDs
            DataManager.sharedInstance.initializeMatchScores()
                        
        }
        
        // Load in all of the bookIDs
        self.server.fetchBooks_allIDs() {(bookList) in
            // Completion closure code:
            // Execute based on closure to ensure that data is available after server query
            print("number of Ids we have \(bookList.count)")
            DataManager.sharedInstance.bookIDs = server.cachedBookIDs
            DataManager.sharedInstance.initializeBookScores()
            
            doneWithLoading = true
            
        }
        
    }
}

struct OpenAppView_Previews: PreviewProvider {
    static var previews: some View {
        OpenAppView()
    }
}
