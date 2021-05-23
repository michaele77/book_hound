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
    @State var imgData = Data() // Image("loadingImg")
    @State var altImage = UIImage(data: try! Data(contentsOf: URL(string: "https://i.stack.imgur.com/Xs4RX.jpg")!))!

//    @State var imgData = Data(base64Encoded: DataManager.sharedInstance.cachedBook.imageBinary)
    @State var imgString = DataManager.sharedInstance.cachedBook.title
//    @State var myUIImage =
    
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
//                Image(imgString)
//                UIImage(data: imgData ?? Data())
                Button(action: {
                    let topID = DataManager.sharedInstance.sortedBookKeys[0]
                    print("We will be looking at \(topID)")
                    self.server.fetchBook_byID(bookID: topID) {thisBook in
                        imgData = Data(base64Encoded: thisBook.imageBinary)!
                        
                    }
                }) { Text("Image Button") }
                
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
            
            
            
            
            
        }.onAppear(perform: loadingDebugFunc)
    }
    
    
    func loadingDebugFunc() {
        print("~~~~~~Loading Swipe Engine page...")
        print("         ~~Testing our Data manager cache:")
        print("         ~~ID: \(DataManager.sharedInstance.cachedBook._id ?? -7), Title \(DataManager.sharedInstance.cachedBook.title ?? "NOPE")")
    }
    
    
 
}
    



struct SwipeEngineView_Previews: PreviewProvider {
    static var previews: some View {
        SwipeEngineView()
    }
}
