#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    int A, B, C, k, x;
    cin >> A >> B >> C >> k >> x;
    
    int ans = 0;
    for (int a = 0; a <= k; a++) {
        for (int b = 0; b <= k - a; b++) {
            int c = k - a - b;
            int flour = A + a * x;
            int egg = B + b * x;
            int milk = C + c * x;
            
            int t1 = flour / 30;
            int t2 = egg / 2;
            int t3 = milk / 50;
            
            int t = min({t1, t2, t3});
            if (t > ans) {
                ans = t;
            }
        }
    }
    
    cout << ans;
    return 0;
}