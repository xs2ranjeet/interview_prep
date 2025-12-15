#include <unordered_map>
#include <mutex>

class LRUCache {
private:
    struct Node {
        int key;
        int value;
        Node* prev;
        Node* next;
        Node(int k, int v) : key(k), value(v), prev(nullptr), next(nullptr) {}
    };

    int capacity;
    std::unordered_map<int, Node*> cache;
    Node* head;   // dummy head
    Node* tail;   // dummy tail
    std::mutex mtx;

    // Add node right after head (Most Recently Used)
    void addToFront(Node* node) {
        node->next = head->next;
        node->prev = head;
        head->next->prev = node;
        head->next = node;
    }

    // Remove a node from the list
    void removeNode(Node* node) {
        Node* p = node->prev;
        Node* n = node->next;
        p->next = n;
        n->prev = p;
    }

    // Move an existing node to the front
    void moveToFront(Node* node) {
        removeNode(node);
        addToFront(node);
    }

    // Remove LRU (node before tail)
    Node* removeLRU() {
        Node* lru = tail->prev;
        removeNode(lru);
        return lru;
    }

public:
    LRUCache(int cap) : capacity(cap) {
        head = new Node(-1, -1);  // dummy head
        tail = new Node(-1, -1);  // dummy tail
        head->next = tail;
        tail->prev = head;
    }

    // Thread-safe get
    int get(int key) {
        std::lock_guard<std::mutex> lock(mtx);

        if (cache.find(key) == cache.end())
            return -1;

        Node* node = cache[key];
        moveToFront(node);
        return node->value;
    }

    // Thread-safe put
    void put(int key, int value) {
        std::lock_guard<std::mutex> lock(mtx);

        if (cache.find(key) != cache.end()) {
            Node* node = cache[key];
            node->value = value;
            moveToFront(node);
            return;
        }

        if (cache.size() == capacity) {
            Node* lru = removeLRU();
            cache.erase(lru->key);
            delete lru;
        }

        Node* node = new Node(key, value);
        cache[key] = node;
        addToFront(node);
    }

    ~LRUCache() {
        Node* curr = head;
        while (curr) {
            Node* next = curr->next;
            delete curr;
            curr = next;
        }
    }
};
