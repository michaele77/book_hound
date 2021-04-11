//
//  DraggingDotView.swift
//  FoodTracker
//
//  Created by Michael Ershov on 4/10/21.
//

import SwiftUI

struct DraggingDotView: View {
    
    // Class properties
    @State var thisoffset = CGSize.zero
    @State var isDragging = false
    @State var message = "Long Press then Drag"
    
    
    var body: some View {
        let longPress = LongPressGesture()
            .onEnded { _ in withAnimation {
                    message = "Now drag me"
                    isDragging = true
                }
                
            }

        let drag = DragGesture()
            .onChanged {
            value in thisoffset = value.translation
            }
            .onEnded { _ in withAnimation {
                    message = "Success!"
                    thisoffset = .zero
                    isDragging = false
                }
            }

        let combined = longPress.sequenced(before: drag)

        Circle()
            .fill(Color.red)
            .frame(width:50, height:50)
            .scaleEffect(isDragging ? 1.5: 1)
            .offset(thisoffset)
            .gesture(combined)
        
        
    }
    
    

}

//        Text(message)
//            .gesture(combined)
//            .offset(self.offset)
//
    
    
    
        
//        let dragGesture = DragGesture().onChanged { value in self.offset = value.translation }.onEnded { _ in withAnimation {
//            self.offset = .zero
//            self.isDragging = false
//        }
//        }
//
//
//        let pressGesture = onLongPressGesture() {
//            withAnimation {
//                self.isDragging = true
//            }
//        }
//
//        let combined = pressGesture.sequenced(before: dragGesture)
//
//        return Circle() .fill(Color.red) .frame(width: 70, height: 30) .scaleEffect(isDragging ? 1.5: 1) .offset(offset) .gesture(DragGesture)
//
//        Text(/*@START_MENU_TOKEN@*/"Hello, World!"/*@END_MENU_TOKEN@*/)


struct DraggingDotView_Previews: PreviewProvider {
    static var previews: some View {
        DraggingDotView()
    }
}
