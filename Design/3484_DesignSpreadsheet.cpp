//https://leetcode.com/problems/design-spreadsheet/
#include<bits/stdc++.h>
using namespace std;

class Spreadsheet {
    vector<vector<int>> sheet;
public:
    Spreadsheet(int rows) {
        sheet = vector<vector<int>>(rows+1, vector<int>(26,0))
    }
    
    void setCell(string cell, int value) {
        auto [row, col] = getRow(cell);
        if(col != -1) {
            sheet[row][col] = value;
        }
    }
    
    void resetCell(string cell) {
        auto [row, col] = getRow(cell);
        if(col != -1) {
            sheet[row][col] = 0;
        }
    }
    
    int getValue(string formula) {
        if(formula[0] != '=')
            return -1;
        size_t pos1 = formula.find("+")
        string first = formula.substr()
    }
private:
    pair<int, int> getRow(string cell) {
        // A10 ... B1000
        int pos = 0;
        int col = -1;
        if(cell[0] >= 'A' and cell[0] <= 'Z') {
            col = cell[0] - 'A';
            pos++;
        }
        int row = stoi(cell.substr(pos));
        return {row, col};
    }
};

/**
 * Your Spreadsheet object will be instantiated and called as such:
 * Spreadsheet* obj = new Spreadsheet(rows);
 * obj->setCell(cell,value);
 * obj->resetCell(cell);
 * int param_3 = obj->getValue(formula);
 */