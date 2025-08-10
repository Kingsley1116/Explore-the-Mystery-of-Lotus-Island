#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <climits>

using namespace std;

struct Point {
    int x, y, s, e, t;
};

int distance(const Point& a, const Point& b) {
    double dx = a.x - b.x;
    double dy = a.y - b.y;
    return (int)sqrt(dx*dx + dy*dy);
}

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
    
    // dp[mask][i] = pair
    vector<vector<pair<int, int>>> dp(1 << n, vector<pair<int, int>>(n, {-1, INT_MAX}));
    
    // 从起点直接到每个景点
    for (int i = 0; i < n; ++i) {
        int walkTime = distanceFromStart(points[i]);
        if (walkTime <= points[i].e - points[i].t && walkTime >= points[i].s) {
            dp[1 << i][i] = {1, walkTime + points[i].t};
        }
    }
    
    for (int mask = 0; mask < (1 << n); ++mask) {
        for (int i = 0; i < n; ++i) {
            if (!(mask & (1 << i))) continue;
            if (dp[mask][i].first == -1) continue;
            
            for (int j = 0; j < n; ++j) {
                if (mask & (1 << j)) continue;
                
                int currentTime = dp[mask][i].second;
                int walkTime = distance(points[i], points[j]);
                int arriveTime = currentTime + walkTime;
                
                if (arriveTime <= points[j].e - points[j].t && arriveTime >= points[j].s) {
                    int newMask = mask | (1 << j);
                    int newCount = dp[mask][i].first + 1;
                    int newTime = arriveTime + points[j].t;
                    
                    if (newCount > dp[newMask][j].first || 
                        (newCount == dp[newMask][j].first && newTime < dp[newMask][j].second)) {
                        dp[newMask][j] = {newCount, newTime};
                    }
                }
            }
        }
    }
    
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
