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
    let header_string =
        "What are your favorite books?"
    let sub_header_string =
        "(You can enter more than one!)"
    
    let dbManager = DBManager()
    
    
    var body: some View {
//        Text(/*@START_MENU_TOKEN@*/"Hello, World!"/*@END_MENU_TOKEN@*/)
        
        
        
        NavigationView {
            VStack(alignment: .leading) {
                
                Spacer()

                Text(header_string)
                    .bold()
                    .padding(.horizontal)
                    .font(.system(size: 25))
                Text(sub_header_string)
                    .padding(.horizontal)
                TextField("Enter book name...", text: $user_input)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding(.horizontal)
                
                Spacer()
                Spacer()
                Spacer()
                
                
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
                    
                }
                
                Button(action: {
                    printString = String(dbManager.countRows())
//                    printString = dbManager.dbPath
                    
                    
//                    dbManager.printPath()
                }) {
                    Text("Debug button")
                }
                
                Text("DEBUG PRINT: " + printString)
            
            }
                
            
        }
        
        

    }
}

struct initialSelectionView_Previews: PreviewProvider {
    static var previews: some View {
        initialSelectionView()
    }
}
