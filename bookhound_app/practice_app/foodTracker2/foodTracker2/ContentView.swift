//
//  ContentView.swift
//  foodTracker2
//
//  Created by Michael Ershov on 4/8/21.
//

import SwiftUI

struct ContentView: View {
    @Binding var document: foodTracker2Document

    var body: some View {
        TextEditor(text: $document.text)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView(document: .constant(foodTracker2Document()))
    }
}
