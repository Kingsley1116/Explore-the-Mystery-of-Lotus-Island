#include <iostream>
#include <string>
#include <vector>
using namespace std;

pair<string, int> divideBy100(string num) {
    if (num == "0") {
        return {"0", 0};
    }
    string quotient = "";
    int remainder = 0;
    for (char c : num) {
        int digit = c - '0';
        remainder = remainder * 10 + digit;
        if (remainder >= 100) {
            quotient += ('0' + remainder / 100);
            remainder %= 100;
        } else {
            if (!quotient.empty()) {
                quotient += '0';
            }
        }
    }
    if (quotient.empty()) {
        quotient = "0";
    }
    return {quotient, remainder};
}

string addSmall(string num, int n) {
    if (n == 0) {
        return num;
    }
    if (num == "") {
        return to_string(n);
    }
    int carry = n;
    string result = num;
    int i = result.size() - 1;
    while (carry > 0 && i >= 0) {
        int digit = result[i] - '0';
        digit += carry;
        carry = digit / 10;
        digit %= 10;
        result[i] = digit + '0';
        i--;
    }
    if (carry > 0) {
        result = to_string(carry) + result;
    }
    return result;
}

int main() {
    string M;
    cin >> M;

    if (M.empty()) {
        cout << 0 << endl;
        return 0;
    }

    if (M.back() != '0') {
        cout << -1 << endl;
        return 0;
    }

    M.pop_back();
    if (M.empty()) {
        M = "0";
    }

    auto [Q, R] = divideBy100(M);

    vector<int> coins_small = {50, 10, 5, 1};
    int count_small = 0;
    int rest = R;
    for (int coin : coins_small) {
        count_small += rest / coin;
        rest %= coin;
    }

    string total = addSmall(Q, count_small);
    cout << total;

    return 0;
}
