//
//  SwipeEngineView.swift
//  BookHound
//
//  Created by Michael Ershov on 4/11/21.
//

import SwiftUI
//import Alamofire


struct SwipeEngineView: View {
//    @State var bookJSON
    
    let server = serverLink()
    @State var printWeight = -7
    @State var printWeight2 = -3
//    @State var returnedJSON: Book = Book()
//    let varToPass_1: String
    
    var body: some View {
        VStack {
            Spacer()
            
            /*
               ++++++++++++++++++++++++++++++++++
               +  UI ELEMENT: TO ENGINE BUTTON  +
               ++++++++++++++++++++++++++++++++++
             */
            Text("Swipe Engine page")
                .foregroundColor(.gray)
            
            // ++++++++++++++++++++++++++++++++++
            
            
            
            /*
               ++++++++++++++++++++++++++++++++++
               +   UI ELEMENT: MAIN BOOK VIEW   +
               ++++++++++++++++++++++++++++++++++
             */
            // This will be the main book recommendation view
            // At first, let's just show the top book in sortedMatches
            
            
            // ++++++++++++++++++++++++++++++++++
            
            
            
            Spacer()
            
            
            
            /*
               ++++++++++++++++++++++++++++++++++
               +   DEBUG PRINTS AND BUTTONS    +
               ++++++++++++++++++++++++++++++++++
             */
            Button(action: {
                server.fetchBook_byID(bookID: 3) { (bookData) in
                    // Closure completion code
                    print("     -->we are inside the button!!")
                    print("     --> " + String(server.cachedBook.genreWeight))
                    printWeight = server.cachedBook.genreWeight
                    
                }
                
            }) {
                Text("Debug button: " + String(printWeight))
            }
            
            
            Text(DataManager.sharedInstance.testString)
                .foregroundColor(.green)
            
            
            Button(action: {
                self.server.fetchUsers_allIDs() {(userList) in
                    printWeight2 = userList.count
                    print("Finished user closure, have \(printWeight2) users")
                    
                }
                
            }) {
                Text("Debug button for Userlist: " + String(printWeight2))
            }
            
            // ++++++++++++++++++++++++++++++++++
            
            
            
            Spacer()
            
            
        }
        
    }
 
}
    



struct SwipeEngineView_Previews: PreviewProvider {
    static var previews: some View {
        SwipeEngineView()
    }
}
