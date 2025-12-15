#include<bits/stdc++.h>
using namespace std;

class Product {
    string code;
    string name;
    double price;

    public:
    Product(...){}
};

class InventoryItem {
    shared_ptr<Product> product;
    int quantity;
public:
    int getQuantity() const { return quantity; }
    void decreaseQuantity() {
        if(quantity > 0)
            quantity--;
    }
    void increaseQuantity(int count) {
        quantity += count;
    }
    bool isAvailable() const {
        return quantity > 0;
    }
};

class Inventory {
    unordered_map<string, shared_ptr<InventoryItem>> items;
public:
    void addProduct(shared_ptr<Product> product, int quantity) {
        items[product->getCode()] = make_shared<InventoryItem>(product, quantity);
    }

    shared_ptr<InventoryItem> getItem(string productCode) {
        if(items.count(productCode) == 0)
            return nullptr;
        return items[productCode];
    }

    bool isAvailable(string productCode) {
        auto item = getItem(productCode);
        return item != nullptr and item->isAvailable();
    }

    void updateQuantity(string productCode, int quantity) {
        auto item = getItem(productCode);
        if(item != nullptr) {
            item->updateQuantity(quantity);
        }
    }

    void displayInventory(){}
};

class VendingMachine;

class VendingMachineState {
    public:
    virtual ~VendingMachineState() {}
    virtual void insertMoney(VendingMachine *machine, double amount) = 0;
    virtual void selectProduct(VendingMachine *machine, string productCode) = 0;
    virtual void dispenseProduct(VendingMachine *machine) = 0;
    virtual void returnMoney(VendingMachine *machine) = 0;
};

class IdleState: public VendingMachineState {
    public:
    void insertMoney(VendingMachine *machine, double amount) { 
        machine->addMoney(amount);
        machine->setState(machine->getHasMoneyState());
    }
    void selectProduct(VendingMachine *machine, string productCode){
        //
    }
    void dispenseProduct(VendingMachine *machine) {
        //
    }
    void returnMoney(VendingMachine *machine) {
        //
    }
};

class HasMoneyState: public VendingMachineState {
    public:
    void insertMoney(VendingMachine *machine, double amount) { 
        machine->addMoney(amount);
    }
    void selectProduct(VendingMachine *machine, string productCode){
        auto inventory = machine->getInventory();
        if(!inventory->isAvailable(productcode))  {
            return;
        }

        auto item = inventory->getItem(productcode);
        auto product = item->getProduct();
        if(machine->getCurrentAmount() < product->getAmount()) {
            return;
        }
        machine->setSelectProduct(product);
        machine->setState(machine->getDispenseState());
        machine->dispenseState();
    }
    void dispenseProduct(VendingMachine *machine) {

    }
    void returnMoney(VendingMachine *machine) {
        machine->setCurrentAmount(0);
        machine->setState(machine->getIdleState());
    }
};

class DispenseState: public VendingMachineState {
    public:
    void insertMoney(VendingMachine *machine, double amount) { 

    }
    void selectProduct(VendingMachine *machine, string productCode){

    }
    void dispenseProduct(VendingMachine *machine) {
        auto product = machine->getProduct();
        auto inventory = machine->getInventory();

        auto item = inventory->getItem(prodcut->getProductCode());
        item->decreaseQuantity();

        double change = machine->getCurrentAmount() - product->getPrice();
        if(change > 0) {

        }
        machine->setCurrentAmount(0);
        machine->setSelectedProduct(nullptr);
        machine->setState(machine->getIdleState());
    }
    void returnMoney(VendingMachine *machine) {
        
    }
};

class VendingMachine {
    shared_ptr<VendingMachineState> idleState, hasMoneyState, dispenseState, currentState;
    shared_ptr<Inventory> inventory;
    double currentAmount = 0.0;
    shared_ptr<Product> selectedProduct;

public:
    VendingMachine(): currentAmounnt(0), selectedProduct(nullptr) {
        idleState = make_shared<IdleState>();
        hasMoneyState = make_shared<HasMoneyState>();
        dispenseState = make_shared<DispenseState>();
        currentState = idleState;
        inventory = make_shared<Inventory>();
    }

    void addProduct(shared_ptr<Product> product, int quatity) {
        inventroy->addProduct(product, quantity);
    }

    void insertMoney(double amount) {
        currentState->insertMoney(this, amount);
    }

    void selectProduct(string productCode) {
        currentState->selectProduct(this, productCode);
    }

    void dispenseProduct() {
        currentState->dispenseProduct(this);
    }

    void returnMoney() {
        currentState->returnMoney();
    }

    void displayProduct() {
        inventory->displayInventory();
    }


    void setState(shared_ptr<VendingMachineState> state) {
        currentState =state;
    }
    void addMoney(double amount) {
        currentAmount += amount;
    }

    void setCurrentAmount(double amount) {
        currentAmount = amount;
    }

    void setSelectedProduct(shared_ptr<Product> product) {
        selectedProduct = product;
    }
};