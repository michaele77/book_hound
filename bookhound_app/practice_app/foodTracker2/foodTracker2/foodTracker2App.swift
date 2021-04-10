//
//  foodTracker2App.swift
//  foodTracker2
//
//  Created by Michael Ershov on 4/8/21.
//

import SwiftUI

@main
struct foodTracker2App: App {
    var body: some Scene {
        DocumentGroup(newDocument: foodTracker2Document()) { file in
            ContentView(document: file.$document)
        }
    }
}
