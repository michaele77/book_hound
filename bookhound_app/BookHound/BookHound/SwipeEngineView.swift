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
    let defaultImg = UIImage(imageLiteralResourceName: "loadingImg")
    @State var printWeight = -7
    @State var printWeight2 = -3
    @State var imgData = Data() // Image("loadingImg")
    @State var altImage = UIImage(imageLiteralResourceName: "loadingImg")
    @State var imgString = DataManager.sharedInstance.cachedBook.title
    
    // Now let's instantiate our predefined constants that increment/decrement scores
    // CHECK! TODO: put these in their own config file! Also do that with the start update var in the initialization scores
    let read_bad    = ParamConfig.read_bad
    let read_good   = ParamConfig.read_good
    let notrd_bad   = ParamConfig.notread_bad
    let notrd_good  = ParamConfig.notread_good
    
    
    var body: some View {
        
        VStack {
            Text(imgString)
//            Image(uiImage: altImage)
//            Image(uiImage: UIImage(data: imgData ?? Data())!)
//            Image(uiImage: UIImage(data: imgData!)!)
//            UIImage(data: imgData!)
            
            Button(action: {
                
            }) { Text("North Button") }
            
            HStack {
                Button(action: {
                    
                }) { Text("East Button") }
                
                // ~~DISPLAY THE IMAGE~~
                Image(uiImage: altImage)
                // ~~DISPLAY THE IMAGE~~
                
                Button(action: {
                    
                }) { Text("West Button") }
            }
            
            Button(action: {
                
            }) { Text("South Button") }
            
            
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
            
            
            Button(action: {
                self.server.fetchUsers_allIDs() {(userList) in
                    printWeight2 = userList.count
                    print("Finished user closure, have \(printWeight2) users")
                    
                }
                
            }) {
                Text("Debug button for Userlist: " + String(printWeight2))
            }
            
            // ++++++++++++++++++++++++++++++++++
            
            
            
            
            
        }.onAppear(perform: loadingFunc)
    }
    
    
    func loadingFunc() {
        // Do initial loads from the favorite selector books
        DataManager.sharedInstance.sortMatchKeys()
        DataManager.sharedInstance.sortBookKeys() { topBook in
            imgString = topBook.title
            imgData = Data(base64Encoded: topBook.imageBinary)!
            if topBook.fullParameter {
                altImage = UIImage(data: imgData)!
            } else {
                altImage = defaultImg
            }
            
        }
    }
    
    
 
}
    



struct SwipeEngineView_Previews: PreviewProvider {
    static var previews: some View {
        SwipeEngineView()
    }
}
