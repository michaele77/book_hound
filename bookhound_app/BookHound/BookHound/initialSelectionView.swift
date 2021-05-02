//
//  initialSelectionView.swift
//  BookHound
//
//  Created by Michael Ershov on 4/10/21.
//

import SwiftUI

struct initialSelectionView: View {
    // initialSelectorView class parameters
    @State var user_input = ""
    @State var printString = ""
    @State var favBookList: [String] = [] //["first"]
    
    
    let header_string =
        "What are your favorite books?"
    let sub_header_string =
        "(You can enter more than one!)"
    
    let varToPass_1 = "test string here!"
    let server = serverLink()

    
    var body: some View {
        
        
        NavigationView {
            VStack(alignment: .leading) {

                Text(header_string)
                    .bold()
                    .padding(.horizontal)
                    .font(.system(size: 25))
                Text(sub_header_string)
                    .padding(.horizontal)
                TextField("Enter book name...", text: $user_input)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding(.horizontal)
                
                
                // In this button, we want to add books entered in the textfield
                // Should clear text, add book to "liked list", and display below
                Button(action: {
                    favBookList.append(user_input)
                    user_input = ""
                    
                }) {
                    Text("Add book")
                        .font(.title)
                        .padding(.horizontal)
                        .foregroundColor(.white)
                        .background(Color(
                        UIColor.systemGray))
                        .cornerRadius(20)
                        .frame(maxWidth: .infinity)
                }
        
                
                Form {
                    Section(header: Text("Fav Books")) {
                        ForEach(favBookList, id: \.self) { curStr in
                            Text(String(curStr))
                                .padding()
                        }
                    }
                }
                
                
                Spacer()
                
                
                // NOTE: need to generate DataManager upon pressing the navigationLink
                // Need to use simultaneousGesture or isActive to perform action while navigating away
                NavigationLink(
                    destination: MainContentView()) {
                    Text("To Engine >>")
                        .font(.title)
                        .padding(.horizontal)
                        .foregroundColor(.white)
                        .background(Color(
                        UIColor.systemBlue))
                        .cornerRadius(20)
                        .frame(maxWidth: .infinity)
                    
                }.simultaneousGesture(TapGesture().onEnded{
                    DataManager.sharedInstance.testString = "test123"
                    let printVar = server.cachedUserIDs.count
                    print("my datamanager list is \(printVar) long")
                })

                
//                Button(action: {
//
//                    if (printString == "") {
//                        printString = "XXX temporary string XXX"
//                    } else {
//                        printString = "1"
//                    }
//
//
////                    printString =
////                        String(dbManager.countRows())
////                    printString = dbManager.dbPath
//
//
////                    dbManager.printPath()
//                }) {
//                    Text("Debug button")
//                }
                
                Text("DEBUG PRINT: " + printString)
                Text("User input print: " + user_input)
                Text(" --> Last char: " + String(user_input.last ?? "X"))
            
            }
                
            
        }.onAppear(perform: loadingFunc)

        
    }
    
    
    func loadingFunc() {
    //    let server = serverLink()
        server.fetchUsers_allIDs()
        DataManager.sharedInstance.userIDs = server.cachedUserIDs
        DataManager.sharedInstance.initializeMatchScores()
        print("Finished loading!!")
    }

    
    
}





struct initialSelectionView_Previews: PreviewProvider {
    static var previews: some View {
        initialSelectionView()
    }
}
