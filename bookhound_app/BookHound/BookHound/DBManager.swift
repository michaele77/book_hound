//
//  DBManager.swift
//  BookHound
//
//  Created by Michael Ershov on 4/11/21.
//

import Foundation
import SQLite


class DBManager {
    let dbUrl = Bundle.main.url(forResource: "bookhound_database_golden", withExtension: "db")!
    let dbPath = Bundle.main.url(forResource: "bookhound_database_golden", withExtension: "db")!.path
    
    let dconn = try! Connection(Bundle.main.url(forResource: "chinook", withExtension: "db")!.path)
    
    
    
    
    func printPath() {
        print(dbPath)
    }
    
    func readSQLTable(bookID: Int) -> Binding? {
        do {
//            return -2
//            var rawNum = try dconn.scalar("SELECT count(*) FROM customers")
            for printVal in try dconn.scalar("SELECT count(*) FROM customers") {
                print(prinVal[0])
            }
            return rawNum
//            return State(initialValue: rawNum.wrappedValue)
            
        } catch {
            return -1
        }
        
        
        

        
    }
    
}




