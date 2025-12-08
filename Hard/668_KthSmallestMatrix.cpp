class Solution {
public:
    int findKthNumber(int m, int n, int k) {
        int lo = 1, hi = m*n;
        auto countLessEqual = [&](int mid) -> bool {
            int count = 0;
            for(int i = 0; i< m; i++)
                count += min(mid/i, n);
            return count;
        };

        while(lo < hi) {
            int mid = lo + (hi - lo)/2;
            if(countLessEqual(mid) < k)
                lo = mid+1;
            else
                hi = mid;
        }
        return lo;
    }
};