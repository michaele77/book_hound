//
//  ContentView.swift
//  FoodTracker
//
//  Created by Michael Ershov on 4/8/21.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        ZStack {
            
            
            Image("meme_im").resizable().aspectRatio (CGSize(width:0.5, height: 0.7), contentMode: .fit)
            
            HStack {
                Spacer()
                
                Text("This is Michael!")
                    .padding(7)
                    .accentColor(.blue)
                    .foregroundColor(Color(UIColor.systemBlue))
                    .background(Color(UIColor.systemGray3))
                
                Spacer()
                
                Text("Whats good baby") .foregroundColor(.white).bold().font(.system(size:45))
                
                Spacer()
            }
            
            
            
            
        }
        
    }
    
    
    
//    Button(action: /*@START_MENU_TOKEN@*//*@PLACEHOLDER=Action@*/{}/*@END_MENU_TOKEN@*/) {
//        /*@START_MENU_TOKEN@*//*@PLACEHOLDER=Content@*/Text("Button")/*@END_MENU_TOKEN@*/
//    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
