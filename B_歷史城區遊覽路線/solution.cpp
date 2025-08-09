#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <climits>

using namespace std;

struct Point {
    int x, y, s, e, t;
};

// 计算两点间距离并向下取整
int distance(const Point& a, const Point& b) {
    double dx = a.x - b.x;
    double dy = a.y - b.y;
    return (int)sqrt(dx*dx + dy*dy);
}

// 计算从起点(0,0)到景点的距离
int distanceFromStart(const Point& p) {
    return (int)sqrt(p.x*p.x + p.y*p.y);
}

int main() {
    int n;
    cin >> n;
    
    vector<Point> points(n);
    for (int i = 0; i < n; ++i) {
        cin >> points[i].x >> points[i].y >> points[i].s >> points[i].e >> points[i].t;
    }
    
    // dp[mask][i] = pair(最多访问景点数, 最少总耗时)
    // mask是状态压缩的二进制数，表示已访问的景点
    vector<vector<pair<int, int>>> dp(1 << n, vector<pair<int, int>>(n, {-1, INT_MAX}));
    
    // 初始化：从起点直接到每个景点
    for (int i = 0; i < n; ++i) {
        int walkTime = distanceFromStart(points[i]);
        // 检查是否可以游览该景点
        if (walkTime <= points[i].e - points[i].t && walkTime >= points[i].s) {
            dp[1 << i][i] = {1, walkTime + points[i].t};
        }
    }
    
    // 状态转移
    for (int mask = 0; mask < (1 << n); ++mask) {
        for (int i = 0; i < n; ++i) {
            // 如果当前状态下i未被访问，跳过
            if (!(mask & (1 << i))) continue;
            // 如果当前状态不可达，跳过
            if (dp[mask][i].first == -1) continue;
            
            // 尝试访问所有未访问的景点
            for (int j = 0; j < n; ++j) {
                if (mask & (1 << j)) continue; // j已访问，跳过
                
                int currentTime = dp[mask][i].second;  // 当前时间（完成景点i的游览）
                int walkTime = distance(points[i], points[j]);  // 从i到j的步行时间
                int arriveTime = currentTime + walkTime;  // 到达j的时间
                
                // 检查是否可以游览景点j
                if (arriveTime <= points[j].e - points[j].t && arriveTime >= points[j].s) {
                    int newMask = mask | (1 << j);
                    int newCount = dp[mask][i].first + 1;
                    int newTime = arriveTime + points[j].t;
                    
                    // 更新状态
                    if (newCount > dp[newMask][j].first || 
                        (newCount == dp[newMask][j].first && newTime < dp[newMask][j].second)) {
                        dp[newMask][j] = {newCount, newTime};
                    }
                }
            }
        }
    }
    
    // 找到最优解
    int maxCount = 0;
    int minTime = 0;
    for (int mask = 0; mask < (1 << n); ++mask) {
        for (int i = 0; i < n; ++i) {
            if (dp[mask][i].first > maxCount || 
                (dp[mask][i].first == maxCount && dp[mask][i].second < minTime)) {
                maxCount = dp[mask][i].first;
                minTime = dp[mask][i].second;
            }
        }
    }
    
    cout << maxCount << " " << minTime << endl;
    
    return 0;
}
