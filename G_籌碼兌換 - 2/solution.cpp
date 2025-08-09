#include <iostream>
#include <vector>
#include <climits>

using namespace std;

int main() {
    int M;
    cin >> M;
    
    // 检查金额是否能被10整除（因为所有筹码都是10的倍数）
    if (M % 10 != 0) {
        cout << -1 << endl;
        return 0;
    }
    
    // 转换为目标金额（除以10，简化计算）
    int target = M / 10;
    
    // 筹码面额（已除以10）：10元->1, 50元->5, 100元->10, 500元->50, 1000元->100
    vector<int> denoms = {1, 5, 10, 50, 100};
    vector<int> counts(5);
    
    for (int i = 0; i < 5; ++i) {
        cin >> counts[i];
    }
    
    // 动态规划数组：dp[i]表示凑出i元所需的最少筹码数
    vector<int> dp(target + 1, INT_MAX);
    dp[0] = 0;  // 凑出0元需要0个筹码
    
    // 处理每种面额的筹码
    for (int i = 0; i < 5; ++i) {
        int d = denoms[i];
        int k = counts[i];
        
        // 多重背包：从大到小遍历以避免重复使用超过限制的筹码
        for (int j = target; j >= 0; --j) {
            if (dp[j] != INT_MAX) {
                // 尝试使用x个当前面额的筹码
                for (int x = 1; x <= k; ++x) {
                    int next = j + x * d;
                    if (next > target) {
                        break;  // 超过目标金额，无需继续尝试
                    }
                    if (dp[next] > dp[j] + x) {
                        dp[next] = dp[j] + x;
                    }
                }
            }
        }
    }
    
    // 输出结果
    if (dp[target] == INT_MAX) {
        cout << -1 << endl;
    } else {
        cout << dp[target] << endl;
    }
    
    return 0;
}
    