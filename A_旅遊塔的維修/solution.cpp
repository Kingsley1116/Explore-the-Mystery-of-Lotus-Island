#include <iostream>
#include <string>
using namespace std;

int main() {
    int m;
    cin >> m;
    
    int height = 0;
    char op;
    int x;
    
    for (int i = 0; i < m; i++) {
        cin >> op >> x;
        if (op == 'U') {
            height += x;
            if (height > 338) {
                height = 338;
            }
        } else if (op == 'D') {
            height -= x;
            if (height < 0) {
                height = 0;
            }
        }
    }
    
    cout << height;
    return 0;
}