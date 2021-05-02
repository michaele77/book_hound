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
//    @State var returnedJSON: Book = Book()
//    let varToPass_1: String
    
    var body: some View {
        VStack {
            Spacer()
            
            Text("Swipe Engine page")
                .foregroundColor(.gray)
            
            Spacer()
            
            Button(action: {
                server.fetchBook_byID(bookID: 3)
                
                print("     -->we are inside the button!!")
                print("     --> " + String(server.cachedBook.genreWeight))
                printWeight = server.cachedBook.genreWeight
            
                
            }) {
                Text("Debug button: " + String(printWeight))
            }
            
            Spacer()
            
            Text(DataManager.sharedInstance.testString)
                .foregroundColor(.green)
            
            Spacer()
            
        }
        
    }
 
}
    



struct SwipeEngineView_Previews: PreviewProvider {
    static var previews: some View {
        SwipeEngineView()
    }
}
