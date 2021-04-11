//
//  MainView.swift
//  FoodTracker
//
//  Created by Michael Ershov on 4/9/21.
//

import SwiftUI

struct MainView: View {
    var body: some View {
        TabView {
            ContentView().tabItem {
                Label("view1", systemImage: "list.dash")
                
            }
            DraggingDotView().tabItem {
                Label("DragTheDot", systemImage: "flame")
            }
            
            
        }
        
        
        
    }
}

struct MainView_Previews: PreviewProvider {
    static var previews: some View {
        MainView()
    }
}
