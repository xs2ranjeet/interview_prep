/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        if(lists.size() == 0)
            return nullptr;
        if(lists.size() == 1)
            return lists[0];
        
        return divideAndConquer(lists, 0, lists.size()-1);
    }

    ListNode *divideAndConquer(vector<ListNode*>& lists, int low, int high) {
        if(low >= high)
            return lists[low];
        int mid = low + (high - low)/2;
        ListNode *left = divideAndConquer(lists, low, mid);
        ListNode *right = divideAndConquer(lists. mid+1, right);

        return merge(left, right);
    } 

    ListNode *merge(ListNode *list1, ListNode *list2) {
        if(!list1)
            return list2;
        if(!list2)
            return list1;
        ListNode dummy = ListNode(0);
        ListNode *node = &dummy;
        while(list1 && list2) {
                if (list1->val < list2->val){
                    node->next = list1;
                    list1 = list1->next;
                } else {
                    node->next = list2;
                    list2 = list2->next;
                }
                node = node->next;
        }
        if(list1)
            node->next = list1;
        if(list2)
            node->next = list2;
        return dummy.next;
    }


    ListNode* mergeKLists2(vector<ListNode*>& lists) {
        if(!list)   return nullptr;
        if(lists.size() == 1)   return lists[0];

        function <bool(ListNode *, ListNode*) cmp = [&](ListNode *a, ListNode *b) {
            return a->val > b->val;
        };
        priority_queue<ListNode *, vector<ListNode*>, decltype(cmp)> minPQ(cmp); 
        for(auto list: lists){
            if(list) {
                minPQ.push(list);
            }
        }
        
        ListNode dummy(0);
        ListNode *node = &dummy;
        while(!minPQ.empty()) {
            ListNode *listNode = minPQ.top(); minPQ.pop();
            node->next = listNode;
            if(listNode->next)
                minPQ.push(listNode->next);
            node = node->next; 
        }
        return dummy.next;
    }
};