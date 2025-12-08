#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
    //nums = [1,3,-1,-3,5,3,6,7], k = 3
    //        0 1  2  3 4 5 6 7  
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        int n = nums.size();
        deque<int> deq;
        vector<int> result;
        int i = 0;
        while(i < n) {
            while(!deq.empty() and (i - deq.front()) >= k)
                deq.pop_front();
            // Maintain decreasing order
            while(!deq.empty() and (nums[deq.back()] < nums[i]))
                deq.pop_back();
            deq.push_back(i);
            if(i - k + 1 >= 0) {
                result.push_back(nums[deq.front()]);
            }
            i++;
        } 
        return result;  
    }
    // maxPQ with lazy delete
    vector<int> maxSlidingWindowPQ(vector<int>& nums, int k) {
        priority_queue<pair<int,int>> maxPQ;
        vector<int> result;
        for(int i = 0; i < nums.size(); i++) {
            maxPQ.push({nums[i], i});
            while(!maxPQ.empty() and (i - maxPQ.top().second) >= k)
                maxPQ.pop();
            if(i >= k-1)
                result.push_back(maxPQ.top.first);
        }
        return result;
    }
};