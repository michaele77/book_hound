//
//  MainContentView.swift
//  BookHound
//
//  Created by Michael Ershov on 4/11/21.
//

import SwiftUI

struct MainContentView: View {
//    let varToPass_1: String
    
    var body: some View {
        TabView {
            SwipeEngineView().tabItem {
                Label("Swipe Engine", systemImage: "book.fill")
            }
            WantToReadView().tabItem {
                Label("Want to Read", systemImage: "heart.circle")
            }
            SettingsView().tabItem {
                Label("Settings", systemImage: "gear")
            }
            
            
        }
    }
}

struct MainContentView_Previews: PreviewProvider {
    static var previews: some View {
        MainContentView()
    }
}
