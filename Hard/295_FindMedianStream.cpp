#include<bits.stdc++.h>
using namespace std;

/*
2, 3,4,5,6,7,8,9, 10, 11, 12
minPQ -> 12, 11, 10, 9,8, 7,
maxPQ -> 2,3, 4, 5, 6
*/

class MedianFinder {
    priority_queue<int, vector<int>, greater<int>> minPQ;  // store right half
    priority_queue<int> maxPQ; // stores left half
public:
    MedianFinder() {
        
    }
    
    void addNum(int num) {
        minPQ.push(num);
        maxPQ.push(minPQ.top());
        minPQ.pop();
        if(maxPQ.size() > minPQ.size() + 1) {
            minPQ.push(maxPQ.top());
            maxPQ.pop();
        }
    }
    
    double findMedian() {
        if ((minPQ.size() + maxPQ.size()) % 2 ==0)
            return (maxPQ.top() + minPQ.top())/2.0;
        return maxPQ.top();
    }
};

/**
 * Your MedianFinder object will be instantiated and called as such:
 * MedianFinder* obj = new MedianFinder();
 * obj->addNum(num);
 * double param_2 = obj->findMedian();
 */