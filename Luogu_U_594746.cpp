#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <string>
using namespace std;

int main() {
    int k;
    cin >> k;
    
    // 存储每条路线的站点
    vector<vector<string>> routes(k);
    // 存储每个站点所属的路线
    unordered_map<string, vector<int>> stationToRoutes;
    // 存储每个站点在每条路线中的位置
    unordered_map<string, unordered_map<int, int>> stationPosInRoute;
    
    for (int i = 0; i < k; i++) {
        int t;
        cin >> t;
        routes[i].resize(t);
        for (int j = 0; j < t; j++) {
            cin >> routes[i][j];
            stationToRoutes[routes[i][j]].push_back(i);
            stationPosInRoute[routes[i][j]][i] = j;
        }
    }
    
    string S, T;
    cin >> S >> T;
    
    // 如果起点就是终点，无需换乘
    if (S == T) {
        cout << 0 << endl;
        return 0;
    }
    
    // 预处理：检查是否有一条路线同时包含起点和终点（可直达，无需换乘）
    for (int r = 0; r < k; r++) {
        bool hasS = false, hasT = false;
        for (const string& station : routes[r]) {
            if (station == S) hasS = true;
            if (station == T) hasT = true;
            if (hasS && hasT) break; // 都找到可以提前退出
        }
        if (hasS && hasT) {
            cout << 0 << endl;
            return 0;
        }
    }
    
    // BFS 寻找最短路径（最少换乘次数）
    queue<pair<string, int>> q;
    unordered_map<string, unordered_map<int, int>> minTransfers;
    
    // 初始化：从起点站可以乘坐所有经过它的路线，初始换乘次数为0
    for (int r : stationToRoutes[S]) {
        q.push({S, r});
        minTransfers[S][r] = 0;
    }
    
    while (!q.empty()) {
        auto [currStation, currRoute] = q.front();
        q.pop();
        
        int currTransfers = minTransfers[currStation][currRoute];
        
        // 检查是否到达终点
        if (currStation == T) {
            cout << currTransfers << endl;
            return 0;
        }
        
        // 在当前路线上移动到相邻站点
        int pos = stationPosInRoute[currStation][currRoute];
        // 向前移动
        if (pos < routes[currRoute].size() - 1) {
            string nextStation = routes[currRoute][pos+1];
            if (!minTransfers[nextStation].count(currRoute) || currTransfers < minTransfers[nextStation][currRoute]) {
                minTransfers[nextStation][currRoute] = currTransfers;
                q.push({nextStation, currRoute});
            }
        }
        // 向后移动
        if (pos > 0) {
            string nextStation = routes[currRoute][pos-1];
            if (!minTransfers[nextStation].count(currRoute) || currTransfers < minTransfers[nextStation][currRoute]) {
                minTransfers[nextStation][currRoute] = currTransfers;
                q.push({nextStation, currRoute});
            }
        }
        
        // 换乘其他路线
        for (int nextRoute : stationToRoutes[currStation]) {
            if (nextRoute != currRoute && (!minTransfers[currStation].count(nextRoute) || currTransfers + 1 < minTransfers[currStation][nextRoute])) {
                minTransfers[currStation][nextRoute] = currTransfers + 1;
                q.push({currStation, nextRoute});
            }
        }
    }
    
    // 无法到达终点
    cout << -1 << endl;
    
    return 0;
}