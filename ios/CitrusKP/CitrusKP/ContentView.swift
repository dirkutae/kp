import SwiftUI

struct ContentView: View {
    var body: some View {
        WebView(resourceName: "index", resourceExtension: "html", subdirectory: "Resources")
            .background(Color(.systemGroupedBackground))
    }
}
