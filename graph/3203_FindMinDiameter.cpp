//https://leetcode.com/problems/find-minimum-diameter-after-merging-two-trees/description/

#include <bits/stdc++.h>
using namespace std;
class Solution {
public:
    int minimumDiameterAfterMerge(vector<vector<int>>& edges1, vector<vector<int>>& edges2) {

        function <vector<vector<int>>(vector<vector<int>>&) buildAdj = [&](vector<vector<int>>& edges) {
            int n = edges.size();
            vector<vector<int>> adj(n+1);
            for(auto& edge : edges) {
                adj[edge[0]].push_back(edge[1]);
                adj[edge[1]].push_back(edge[0]);
            }
            return adj;
        };

        function <pair<int, int>(vector<vector<int>>, int)> = distantNode(vector<vector<int>> &graph, int start) {
            int n = graph.size();
            vector<bool> visited(n+1, false);
            queue<int> que;
            que.push({0,start});
            visited[start] = true;
            int maxDistant = 0, farNode = start;
            while(!que.empty()) {
                auto [dist, node] = que.front(); que.pop();
                maxDistant = dist;
                farNode = node;
                for(auto nei: graph[node]) {
                    if(visited[nei])    continue;
                    visited[nei] = true;
                    que.push({dist+1, nei});
                }
            }
            return {farNode, maxDistant};
        };

        function <int(vector<vector<int>>)> findDiametr = [&](vector<vector<int>> &edges) {
            vector<vector<int>> graph = buildAdj(edge);

            int n = graph.size();
            int start = 0;
            while(start < n and graph[start].empty())
                start++;
            if(start == n)
                return 0;
            auto [node, _] = distantNode(graph, start);
            auto [_ maxDistance] = distantNode(graph, node);
            return maxDistance;
        };

     
        int d1 = findDiameter(edges1);
        int d2 = findDiameter(edges2);
        int r1 = ceil(d1/2), r2 = ceil(d2/2);
        return max({d1, d2, r1+r2+1});
    }
};