#include <iostream>
#include <cstring>
using namespace std;

int ans, n;
string s;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0), cout.tie(0);

    cin >> n;

    for (int i = 0; i < n; i++) {
        cin >> s;
        if (s == "大三巴") ans++;
    }

    cout << ans;
    return 0;
}