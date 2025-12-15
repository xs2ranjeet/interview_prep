#include<bits/stdc++.h>
using namespace std;

class Player {
    public:
    string name;
    int position;
    Player(const string &name, int pos): name(name), position(pos) {}
};

class Cell {
    int position;
public:
    Cell(int pos): position(pos) {}
   int getPosition() const { return position;}
   virtual int getNextPosition(int currentPos) = 0;
   virtual ~Cell() = default; 
};

class NormalCell: public Cell {
public:
    NormalCell(int pos): Cell(pos){}
    int getNextPosition(int currentPos) override {
        return currentPos;
    }
};

class Snake: public Cell {
    int tail;
public:
    Snake(int front, int tail): Cell(front), tail(tail) {}
    int getNextPosition(int pos) override {
        return tail;
    }
};

class Ladder: public Cell {
    int top;
public:
    LadderCell(int bottom, int top): Cell(bottom), top(top) {}
    int getNextPosition(int pos) override {
        return top;
    }
};

class Dice {
    int numDice;
public:
    Dice(int num):numDice(num) {
        srand(time(0));
    }
     int roll() {
        int total = 0;
        for(int i = 0; i < numDice; i++) {
            total += (rand() % 6) +1;
        }
        cout<<"Dice rolled "<< total<<"\n";
        return total;
     }
};


class Board {
    int size;
    vector<shared_ptr<Cell>> cells;

public:
    Board(int s): size(s)
    cells.resize(size+1);
    for(int i = 0; i <= size; i++) {
        cells[i] = make_shared<NormalCell>(i)
    }

    void addSnake(int head, int tail) {
        if(head > tail and head <= size and tail >= 0)
            cells[head] = make_shared<Snake>(head, tail);
    }
    void addLadder(int bottom, int top) {
        if(top > bottom and top <= size and bottom >= 0)
            cells[bottom] = make_shared<Ladder>(bottom, top);
    }

    int getNextPosition(int pos) {
        if(pos > size)  return pos;
        return cells[pos]->getNextPosition(pos);
    }

    int getSize() const {
        return size;
    }
};

class SnakeAndLadderGame {
    shared_ptr<Board> board;
    shared_ptr<Dice> dice;
    queue<shared_ptr<Player>> players;
    int winningPosition;

public:
    SnakeAndLadderGame(int boardSize, int numDice): winningPosition(boardSize) {
        dice = make_shared<Dice>(numDice);
        board = make_shared<Board>(boardSize);
    }

    void addPlayer(shared_ptr<Player> player) {
        players.push(player);
    }
    void addSnake(int head, int tail) {
        board->addSnake(head, tail);
    }

    void addLadder(int bottom, int top) {
        board->addLadder(bottom, top);
    }


    void start() {
        while(players.size() > 1) {
            auto currentPlayer = players.front(); 
            players.pop();

            int diceValue = dice.roll();
            int newPos =  currentPlayer->position + diceValue;
            if(newPos > winningPosition) {
                cout<<" cna;t win\n";
                players.push(currentPlayer);
                continue;
            }
            newPos = board->getNextPosition(newPos);
            currentPlayer->position = newPos;

            if(newPos == winningPosotion) {
                cout<< "won..\n";
                break;
            }
            players.push(currentPlayer);
        }
    }
};