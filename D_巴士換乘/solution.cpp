#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <string>
using namespace std;

int main() {
    int k;
    cin >> k;
    
    vector<vector<string>> routes(k);
    unordered_map<string, vector<int>> stationToRoutes;
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
    
    if (S == T) {
        cout << 0 << endl;
        return 0;
    }
    
    for (int r = 0; r < k; r++) {
        bool hasS = false, hasT = false;
        for (const string& station : routes[r]) {
            if (station == S) hasS = true;
            if (station == T) hasT = true;
            if (hasS && hasT) break;
        }
        if (hasS && hasT) {
            cout << 0 << endl;
            return 0;
        }
    }
    
    queue<pair<string, int>> q;
    unordered_map<string, unordered_map<int, int>> minTransfers;
    
    for (int r : stationToRoutes[S]) {
        q.push({S, r});
        minTransfers[S][r] = 0;
    }
    
    while (!q.empty()) {
        auto [currStation, currRoute] = q.front();
        q.pop();
        
        int currTransfers = minTransfers[currStation][currRoute];
        
        if (currStation == T) {
            cout << currTransfers << endl;
            return 0;
        }
        
        int pos = stationPosInRoute[currStation][currRoute];

        if (pos < routes[currRoute].size() - 1) {
            string nextStation = routes[currRoute][pos+1];
            if (!minTransfers[nextStation].count(currRoute) || currTransfers < minTransfers[nextStation][currRoute]) {
                minTransfers[nextStation][currRoute] = currTransfers;
                q.push({nextStation, currRoute});
            }
        }
        if (pos > 0) {
            string nextStation = routes[currRoute][pos-1];
            if (!minTransfers[nextStation].count(currRoute) || currTransfers < minTransfers[nextStation][currRoute]) {
                minTransfers[nextStation][currRoute] = currTransfers;
                q.push({nextStation, currRoute});
            }
        }
        
        for (int nextRoute : stationToRoutes[currStation]) {
            if (nextRoute != currRoute && (!minTransfers[currStation].count(nextRoute) || currTransfers + 1 < minTransfers[currStation][nextRoute])) {
                minTransfers[currStation][nextRoute] = currTransfers + 1;
                q.push({currStation, nextRoute});
            }
        }
    }
    
    cout << -1 << endl;
    
    return 0;
}

