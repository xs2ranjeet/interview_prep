#include <bits/stdc++.h>
using namespace std;
// https://leetcode.com/problems/closest-subsequence-sum/description/
class Solution {
public:
    int minAbsDifference(vector<int>& nums, int goal) {
        int n = nums.size();
        int halfSize = n/2;
        vector<int> first(nums.begin(), nums.begin()+ halfSize);
        vector<int> second(nums.begin()+ halfSize, nums.end());

        auto getSubSeqSum = [&](vector<int> list) {
            int size = list.size();
            vector<int> sums(1 << size);
            for(int mask = 0; mask < (1 << size); mask++) {
                for(int i = 0; i < size; i++) {
                    if(mask & (1 << i))
                        sums[mask] += list[i];
                }
            }
            return sums;
        };
        vector<int> leftSum = getSubSeqSum(first), rightSum = getSubSeqSum(second);
        sort(rightSum.begin(), rightSum.end());

        int closest_diff = INT_MAX;
        for(int sum1 : leftSum) {
            int needed = goal - sum1;
            auto it = lower_bound(rightSum.begin(), rightSum.end(), needed);
            if(it != rightSum.end()) {
                closest_diff = min(closest_diff, abs(sum1 + *it - goal));
            }
            if( it != rightSum.begin()) {
                closest_diff = min(closest_diff, abs(sum1 + *prev(it) - goal));
            }
        }
        return closest_diff;
    }
};