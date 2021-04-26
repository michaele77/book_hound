//
//  SwipeEngineView.swift
//  BookHound
//
//  Created by Michael Ershov on 4/11/21.
//

import SwiftUI
//import Alamofire


struct SwipeEngineView: View {
//    @State var bookJSON
    
    let server = serverLink()
    
    var body: some View {
        VStack {
            Spacer()
            
            Text("Swipe Engine page")
                .foregroundColor(.gray)
            
            Spacer()
            
            Button(action: {
                server.viewDidLoad()
            }) {
                Text("Debug button")
            }
            
            Spacer()
            
        }
        
        
    }
    
//    func viewDidLoad() {
//        print("I am here")
//
//        AF.request("http://192.168.1.72:8084/fetchBook?bookID=186074").responseJSON {
//            response in
//            print(response.data)
//            let data = String(data: response.data!, encoding: .utf8)
//
//            let dataJSON = JSONDecoder.decode([Book].self, from: )
//
//            print(data!)
//            print("----PARTITION---")
//            print(data.author)
//        }
//
////        let jsonData = try JSONSerialization.data(withJSONObject: metadata)
////
////        // Convert to a string and print
////        if let JSONString = String(data: jsonData, encoding: String.Encoding.utf8) {
////           print(JSONString)
////        }
////
//
//
////        debugPrint(bookJSON)
//    }
    
    
}
    
    
    

//extension SwipeEngineView: DataDelegate {
//    // Lets load in out JSON book file
//    func updateBookView(newArr: String) {
//        do {
//            notesArr = try JSONDecoder.decode(
//        } catch {
//            print("filed to decode!")
//        }
//    }
//}


struct SwipeEngineView_Previews: PreviewProvider {
    static var previews: some View {
        SwipeEngineView()
    }
}
