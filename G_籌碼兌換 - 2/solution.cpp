#include <iostream>
#include <vector>
#include <climits>

using namespace std;

int main() {
    int M;
    cin >> M;
    
    if (M % 10 != 0) {
        cout << -1 << endl;
        return 0;
    }
    
    int target = M / 10;
    
    vector<int> denoms = {1, 5, 10, 50, 100};
    vector<int> counts(5);
    
    for (int i = 0; i < 5; ++i) {
        cin >> counts[i];
    }
    
    vector<int> dp(target + 1, INT_MAX);
    dp[0] = 0;
    
    for (int i = 0; i < 5; ++i) {
        int d = denoms[i];
        int k = counts[i];
        
        for (int j = target; j >= 0; --j) {
            if (dp[j] != INT_MAX) {
                for (int x = 1; x <= k; ++x) {
                    int next = j + x * d;
                    if (next > target) {
                        break;
                    }
                    if (dp[next] > dp[j] + x) {
                        dp[next] = dp[j] + x;
                    }
                }
            }
        }
    }
    
    if (dp[target] == INT_MAX) {
        cout << -1 << endl;
    } else {
        cout << dp[target] << endl;
    }
    
    return 0;
}

    
