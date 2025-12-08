#include <bits/stdc++.h>

#define pii pair<int,int>
using namespace std;
class TaskManager {
    unordered_map<int, pii> tid_pid_uid;
    priority_queue<pii> maxheap;
public:
    TaskManager(vector<vector<int>>& tasks) { 
        // userId, taskId, priority
        for(auto& task : tasks) {
            int uid = task[0], tid = task[1], pri = task[2];
            tid_pid_uid[tid] = {pri, uid};
            maxheap.push({pri, tid});
        }
    }
    
    void add(int userId, int taskId, int priority) {
        tid_pid_uid[taskId] = {priority, userId};
        maxheap.push({priority, taskId});
    }
    
    void edit(int taskId, int newPriority) {
        tid_pid_uid[taskId].first = newPriority;
        maxheap.push({newPriority, taskId});
    }
    
    void rmv(int taskId) {
        tid_pid_uid.erase(taskId);
    }
    
    int execTop() {
        while(!maxheap.empty()) {
            auto [priority, taskId] = maxheap.top(); maxheap.pop();

            if(tid_pid_uid.count(taskId) and tid_pid_uid[taskId].first == priority) {
                int userId = tid_pid_uid[taskId].second;
                tid_pid_uid.erase(taskId);
                return userId;
            }
        }
        return -1;
    }
};

/**
 * Your TaskManager object will be instantiated and called as such:
 * TaskManager* obj = new TaskManager(tasks);
 * obj->add(userId,taskId,priority);
 * obj->edit(taskId,newPriority);
 * obj->rmv(taskId);
 * int param_4 = obj->execTop();
 */