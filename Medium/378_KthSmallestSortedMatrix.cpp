#include <bits/stdc++.h>
using namespace std;

int kthSmallest(vector<vector<int>>& matrix, int k) {
    int rows = matrix.size(), cols = matrix[0].size();
    int lo = matrix[0][0], hi = matrix[rows-1][cols-1];

    auto countLessEqual   = [&](int) -> int {
        int row = rows - 1, col = 0, count = 0;
        while(row >=0 and col < cols) {
            if(matrix[row][col] <= mid) {
                count += row +1;
                col++;
            } else{
                row--;
            }
        }
        return count;
    };

    while(lo < hi) {
        int mid = lo + (hi - lo)/2;
        if(countLessEqual(mid) < k) {
            lo = mid+1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

int kthSmallest(vector<vector<int>>& matrix, int k) {
    int rows = matrix.size(), cols = matrix[0].size();
    if (rows == 0 || cols == 0 || k <= 0) return -1;
    using State = tuple<int,int,int>;
    priority_queue<State, vector<State>, greater<State>> minPQ;
    for(int i = 0; i < min(rows, k); i++) {
        minPQ.push({matrix[i][0], i, 0});
    }

    int ans = 0;
    for(int i = 0; i < k ; i++) {
        auto [current, r, c] = minPQ.top(); minPQ.pop();
        ans = current;
        if(c + 1 < cols){
            minPQ.push({matrix[r][c+1], r, c+1});
        }
    }
    return ans;
}