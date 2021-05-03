//
//  initialSelectionView.swift
//  BookHound
//
//  Created by Michael Ershov on 4/10/21.
//

import SwiftUI

struct initialSelectionView: View {
    // initialSelectorView class parameters
    
    // @State variables
    @State var user_input = ""
    @State var printString = ""
    @State var favBookList: [String] = [] //["first"]
    @State var favBookIDsList: [Int] = []
    @State var textBoxLabel = "Enter book name..."
    
    
    // Other (non mutating) variables
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
                TextField(textBoxLabel, text: $user_input)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding(.horizontal)
                
                
                // In this button, we want to add books entered in the textfield
                // Should clear text, add book to "liked list", and display below
                Button(action: {
                    // TODO: Implement autocorrect based on a pre-loaded list of book names (implement that in dataManager)
                    // TODO: Modify append values, implement lookup query function in serverLink
                    // First check that user_input has something TODO: Update this to checking for book name
                    if (user_input == "") {
                        print("User added invalid input!")
                        textBoxLabel = "Please add valid book ID!"
                        DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
                            textBoxLabel = "Enter book name..."
                        }
                        
                    } else {
                        favBookList.append(user_input)
                        var userInputInt = Int(user_input) ?? -1
                        favBookIDsList.append(userInputInt)
                        DataManager.sharedInstance.updateFavoriteMatch(book: userInputInt)
                        user_input = ""
                    }
                    
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
                    DataManager.sharedInstance.sortMatchKeys()
                    
                })

                
                Text("DEBUG PRINT: " + printString)
                Text("User input print: " + user_input)
                Text(" --> Last char: " + String(user_input.last ?? "X"))
            
            }
                
            
        }.onAppear(perform: loadingFunc)

        
    }
    
    
    func loadingFunc() {
    //    let server = serverLink()
        server.fetchUsers_allIDs()
        print("number of Ids we have \(server.cachedUserIDs.count)")
        
        // Dispatch a delayed, timed functin execution
        // This is because cachedUserIDs will not be available immediately from the server, it is asynchronous
        // Wait some fixed number of seconds
        // TODO: Potentially play with delay here or add in a catch?
        DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
            print("number of Ids we have \(server.cachedUserIDs.count)")
            DataManager.sharedInstance.userIDs = server.cachedUserIDs
            DataManager.sharedInstance.initializeMatchScores()
            print("Timed thread now finished running!")
        }
        
        print("Finished loading!! (timed thread still running)")
    }

    
    
}





struct initialSelectionView_Previews: PreviewProvider {
    static var previews: some View {
        initialSelectionView()
    }
}
