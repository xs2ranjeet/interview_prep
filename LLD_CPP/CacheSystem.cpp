#include <bits/stdc++.h>
using namespace std;

class IStorage {
    public:
    virtual ~IStorage() = default;
    virtual bool contains(int key) = 0;
    virtual int value(int key) = 0;
    virtual void update(int key, int value) = 0;
    virtual void remove(int key) = 0;
    virtual int size() = 0;
    virtual void insert(int key, int value) = 0;
};
class IEviction {
public:
    virtual ~IEviction() = default;
    virtual void update(int key) = 0;
    virtual int evictionKey() = 0;
};
class CacheSystem {
    IStorage *storage;
    IEviction *policy;
    int capacity;
public:
    CacheSystem(int capacity, IStorage *storage, IEviction *eviction): capacity(capacity), storage(storage), policy(eviction) {}

    int get(int key) {
        if(!storage->contains(key))
            return -1;
        policy->update(key);
        return storage->value(key);
    }

    void put(int key, int value) {
        if(storage->contains(key)) {
            storage->update(key, value);
            policy->update(key);
            return;
        }
        if(storage->size() == capacity) {
            int keyToRemove = policy->evictionKey();
            storage->remove(keyToRemove);
        }
        storage->insert(key, value);
        policy->update(key);
    }
};

class LRU: public IEviction {
    list<int> lst;
    unordered_map<int, list<int>::iterator> mp;
public:
    ~LRU() = default;
    void update(int key) override {
        if (mp.count(key)) {
            lst.erase(mp[key]);
        }
        lst.push_front(key);
        mp[key] = lst.begin();
    }
    int evictionKey() override {
        int key = lst.back();
        lst.pop_back();
        mp.erase(key);
        return key;
    }
};

class InMemory: public IStorage {
    unordered_map<int, int> store;
    public:
    ~InMemory() = default;
    bool contains(int key) override {
        return store.count(key);
    }
    int value(int key) override {
        return store[key];
    }
    void update(int key, int value) override {
        store[key] = value;
    }
    void remove(int key) override {
        store.erase(key);
    }
    int size() override {
        return store.size();
    }
    void insert(int key, int value) override {
        update(key, value);
    }
};

int main() {
    InMemory *memory = new InMemory();
    LRU *lru = new LRU();
    CacheSystem *cache = new CacheSystem(2, memory, lru);
    cache->put(2, 10);
    cache->put(3, 8);
    cout<<cache->get(3)<<"\n";
    cache->put(1, 32);
    cout<<cache->get(2)<<"\n";
    return 0;
}