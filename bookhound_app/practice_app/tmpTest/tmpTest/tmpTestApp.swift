//
//  tmpTestApp.swift
//  tmpTest
//
//  Created by Michael Ershov on 4/25/21.
//

import SwiftUI

@main
struct tmpTestApp: App {
    let persistenceController = PersistenceController.shared

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, persistenceController.container.viewContext)
        }
    }
}
