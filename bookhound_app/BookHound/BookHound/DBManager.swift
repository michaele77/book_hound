//
//  DBManager.swift
//  BookHound
//
//  Created by Michael Ershov on 4/11/21.
//

import Foundation
//import SQLite
import SQLite3


class DBManager {
    
    var database:OpaquePointer? = nil // pre-allocate instance variable
    
    let dbPath = Bundle.main.url(forResource: "bookhound_database_graph_1", withExtension: "db")!.path
//    let dbPath = Bundle.main.url(forResource: "chinook", withExtension: "db")!.path
    
    let SQLQuery_countAll = "SELECT COUNT(*) FROM books"
    
    init() {
        self.openDatabase()
    }
        
    
    
    // NOTE: sqlite3 error message constants can be found in sqlite3 docs
    func openDatabase() {
      if sqlite3_open(dbPath, &database) == SQLITE_OK {
        print("Successfully opened connection to database at \(dbPath)")
      } else {
        print("Unable to open database.")
      }
    }
    
    func countRows() -> Int32 {
        var queryStatement: OpaquePointer?
        var count:Int32 = 0
        if sqlite3_prepare(database, SQLQuery_countAll, -1, &queryStatement, nil) == SQLITE_OK {
            while(sqlite3_step(queryStatement) == SQLITE_ROW){
                count = sqlite3_column_int(queryStatement, 0)
                print("\(count)")
            }
            

        }
        return count
    }
    
    
//    func query() {
//      var queryStatement: OpaquePointer?
//      // 1
//      if sqlite3_prepare_v2(database, SQLQuery_countAll, -1, &queryStatement, nil) ==
//          SQLITE_OK {
//        // 2
//        if sqlite3_step(queryStatement) == SQLITE_ROW {
//          // 3
//          let id = sqlite3_column_int(queryStatement, 0)
//          // 4
//          guard let queryResultCol1 = sqlite3_column_text(queryStatement, 1) else {
//            print("Query result is nil")
//            return
//          }
//          let name = String(cString: queryResultCol1)
//          // 5
//          print("\nQuery Result:")
//          print("\(id) | \(name)")
//      } else {
//          print("\nQuery returned no results.")
//      }
//      } else {
//          // 6
//        let errorMessage = String(cString: sqlite3_errmsg(db))
//        print("\nQuery is not prepared \(errorMessage)")
//      }
//      // 7
//      sqlite3_finalize(queryStatement)
//    }
//
    
    
    
    // Old stuff cached below (for now...remove them in a bit)
    
    
    
//    let dbUrl = Bundle.main.url(forResource: "bookhound_database_golden", withExtension: "db")!
//    let dbPath = Bundle.main.url(forResource: "bookhound_database_golden", withExtension: "db")!.path
//
//    let dconn = try! Connection(Bundle.main.url(forResource: "chinook", withExtension: "db")!.path)
//
//
//
//
//    func printPath() {
//        print(dbPath)
//    }
//
//    func readSQLTable(bookID: Int) -> Binding? {
//        do {
////            return -2
////            var rawNum = try dconn.scalar("SELECT count(*) FROM customers")
//            for printVal in try dconn.scalar("SELECT count(*) FROM customers") {
//                print(prinVal[0])
//            }
//            return rawNum
////            return State(initialValue: rawNum.wrappedValue)
//
//        } catch {
//            return -1
//        }
//
//
//
//
//
//    }
//
}




