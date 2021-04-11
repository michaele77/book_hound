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
    let header_string =
        "What are your favorite books?"
    let sub_header_string =
        "(You can enter more than one!)"
    
    
    var body: some View {
//        Text(/*@START_MENU_TOKEN@*/"Hello, World!"/*@END_MENU_TOKEN@*/)
        
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
            Spacer()
            
            Text("DEBUG PRINT: " + user_input)
            
        }
    }
}

struct initialSelectionView_Previews: PreviewProvider {
    static var previews: some View {
        initialSelectionView()
    }
}
