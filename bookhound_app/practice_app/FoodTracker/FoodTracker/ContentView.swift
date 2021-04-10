//
//  ContentView.swift
//  FoodTracker
//
//  Created by Michael Ershov on 4/8/21.
//

import SwiftUI

struct ContentView: View {
    
    @State var button_iter = 0
    @State var rand_num = 0
    
    
    
    var body: some View {
        
        ScrollView {
            
            ZStack {
                
                VStack {
                    Button("Hello bitches") {
                        print("WHATS GOODDD??!?!")
                    }
                    
                    
                    Button(action: {
    //                    button_iter += 1
                        rand_num = Int.random(in: 1...99)
                        button_iter += rand_num
                    }, label: {
                        
                        HStack {
                            Text(String(button_iter))
                            Image(systemName: "pencil")
                            Text("Dis pencis")
                            Image(systemName: "flame.fill")
                            Text(String(rand_num))
                        }
                        
                    })
                    
                    Image("meme_im").resizable().aspectRatio (CGSize(width:0.5, height: 0.7), contentMode: .fill)
                    
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
                    
                    
                    Text("Whats up man now im just gonna write a fuck ton of stuff to take up space so that i can simpyl idbfabidbc sbf kisbdkc bskjdnckj sndfkc sdkcb sjdcj sdkfnc ksdncknsdkcnk sdnckn sdkcn ksdnck jnsdkjcn ksdnck sndkjcn skjdnc kjsdnkcj nsdknc ksdnc kjnsdkjcnksdnckjsndkcnskdjncksnd cksndk cskdcksdckhbqweifdbwidsfbkweb kwedksn kjsndck nsdkn skjdc kjsdckjsdnc jksdnc kjsndck nsdkc nskdc ksdnck sndkc nskdc ksjdnc ksndck nsdkn ksdjnc sd")
                }
                
                
                
            }
            .navigationTitle("Discover...")
            
        }
            
            
        }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        Group {
            ContentView().preferredColorScheme(/*@START_MENU_TOKEN@*/.dark/*@END_MENU_TOKEN@*/)
            ContentView().preferredColorScheme(.light
            )
        }
        
    }
}
