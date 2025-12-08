#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
    int maxRemoval(vector<int>& nums, vector<vector<int>>& queries) {
        priority_queue<int, vector<int>, greater<int>> used_query;
        priority_queue<int> available_query;
        sort(queries.begin(), queries.end());
        int q_pos = 0;
        int applied_count = 0;
        for(int i = 0; i < nums.size(); i++) {
            while(q_pos < queries.size() and queries[q_pos][0] == i) {
                available_query.push(queries[q_pos][1]);
                q_pos++;
            }

            nums[i] -= used_query.size();
            if(nums[i] < 0) nums[i] = 0;

            while(nums[i] > 0 and !available_query.empty() and available_query.top() >= i){
                used_query.push(available_query.top());
                applied_count++;
                nums[i]--;
                available_query.pop();
            }

            if(nums[i] > 0) return -1;

            while(!used_query.empty() and used_query.top() == i)
                used_query.pop();
        }
        return queries.size() - applied_count;
    }
};