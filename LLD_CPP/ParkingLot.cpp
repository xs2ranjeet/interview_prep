#include <bits/stdc++.h>
using namespace std;
//https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/parking-lot.md
/*
Requirements
The parking lot should have multiple levels, each level with a certain number of parking spots.
The parking lot should support different types of vehicles, such as cars, motorcycles, and trucks.
Each parking spot should be able to accommodate a specific type of vehicle.
The system should assign a parking spot to a vehicle upon entry and release it when the vehicle exits.
The system should track the availability of parking spots and provide real-time information to customers.
The system should handle multiple entry and exit points and support concurrent access.
*/
enum VehicleType { Car, Bike, Truck};
enum SpotType { Small, Medium, Large};

class Vehicle {
public:
    string plate;
    VehicleType type;

    Vehicle(const string &plate, VehicleType type)
        : plate(plate), type(type) {}

    virtual ~Vehicle() = default; // safer and cleaner
};

class CarVehicle : public Vehicle {
public:
    CarVehicle(const string &plate)
        : Vehicle(plate, VehicleType::Car) {}

    ~CarVehicle() override = default;
};

class BikeVehicle : public Vehicle {
public:
    BikeVehicle(const string &plate)
        : Vehicle(plate, VehicleType::Bike) {}

    ~BikeVehicle() override = default;
};

class TruckVehicle : public Vehicle {
public:
    TruckVehicle(const string &plate)
        : Vehicle(plate, VehicleType::Truck) {}

    ~TruckVehicle() override = default;
};

class PricingStrategy {
public:
    virtual double fare(VehicleType type, int minutes) = 0;
    virtual ~PricingStrategy() = default;
};



class SimpleHour: public PricingStrategy {
    unordered_map<VehicleType, double> rate;
public:
    SimpleHour(unordered_map<VehicleType, double> hourly): rate(hourly) {}

    SimpleHour() {
        rate[VehicleType::Bike] = 10;
        rate[VehicleType::Car] = 20;
        rate[VehicleType::Truck] = 30;
    }
    double fare(VehicleType type, int minutes) override {
        int hours = (minutes + 59)/ 60;
        return hours * rate[type];
    }

    ~SimpleHour() override = default;

};

class Payment{
    public:
     virtual bool process(double amount) = 0;
     virtual ~Payment() {}
};

class CardPayment: public Payment {
    public:
    bool process(double amount) override {
        cout<<"Paid "<<amount<<" \n";
        return true;
    }
};


class ParkingSpot {
public:
    string id;
    SpotType type;
    bool free;

    ParkingSpot(string id, SpotType type):id(id), type(type), free(true) {}
};

class Ticket{
public:
    string id;
    string plate;
    string spotid;
    int floor;
    SpotType spotType;
    time_t entry;
    time_t exit;
    double amount;

    Ticket(const string& i, const string& p, int floor, SpotType st, const string& spotid): id(i), plate(p), spotType(st), spotid(spotid), entry(time(nullptr)){}

};

class ParkingFloor {
public:
    int id;
    vector<shared_ptr<ParkingSpot>> spots;
    unordered_map<SpotType, atomic<int>> freeCount;
    std::mutex mtx;

    ParkingFloor(int id):id(id) {}

    ParkingFloor(int id, int small, int medium, int large): id(id) {
        for(int i = 0; i < small; i++) {
            string idx = "F" + to_string(id) + "-" + to_string(spots.size() + 1);
            spots.push_back(make_shared<ParkingSpot>(idx, SpotType::Small));
        }
        for(int i = 0; i < medium; i++) {
            string idx = "F" +  to_string(id) + "-" + to_string(spots.size() + 1);
            spots.push_back(make_shared<ParkingSpot>(idx, SpotType::Medium));
        }
        for(int i = 0; i < large; i++) {
            string idx = "F" +  to_string(id) + "-" + to_string(spots.size() + 1);
            spots.push_back(make_shared<ParkingSpot>(idx, SpotType::Large));
        }

        freeCount[SpotType::Small] = small;
        freeCount[SpotType::Medium] = medium;
        freeCount[SpotType::Large] = large;
    }

    void addSpots(SpotType type, int count) {
         for(int i = 0; i < count; i++) {
            string idx = "F" +  to_string(id) + "-" + to_string(spots.size() + 1);
            spots.push_back(make_shared<ParkingSpot>(idx, type));
        }
        freeCount[type] += count;

    }
};

class ParkingLot {
    vector<shared_ptr<ParkingFloor>> floors;
    unordered_map<string, shared_ptr<Ticket>> activeTickets;
    unordered_map<string, string> plateToTicket;
    Payment *payment;
    PricingStrategy *pricing;
public:
    ParkingLot(PricingStrategy *p):pricing(p) {

    }
    void addFloor(shared_ptr<ParkingFloor> floor) {
        floors.push_back(floor);
    }

    static SpotType requiredSpot(VehicleType type) {
        if(type == VehicleType::Bike)   return SpotType::Small;
        if(type == VehicleType::Car) return SpotType::Medium;
        return SpotType::Large;
    }

    static string makeId(const string& prefix) {
        static atomic<unsigned long> seq{1};
        return prefix + to_string(seq.fetch_add(1));
    }


    string park(shared_ptr<Vehicle> vehicle) {
        SpotType need = requiredSpot(vehicle->type);

        for(auto floor: floors) {
            lock_guard<mutex> lock(floor->mtx);

            if(floor->freeCount[need] <= 0) continue;

            for(auto spot: floor->spots) {
                if(spot->free && spot->type == need) {
                    spot->free = false;
                    floor->freeCount[need]--;
                    string tid = makeId("T");
                    auto ticket = make_shared<Ticket>(tid, vehicle->plate, floor->id, spot->type, spot->id);

                    activeTickets[tid] = ticket;
                    plateToTicket[vehicle->plate] = tid;
                    return tid;
                }
            }
        }
        return "";
    }

    bool unpark(shared_ptr<Vehicle> vehicle) {
        if(!plateToTicket.count(vehicle->plate))
            return false;
        string tid = plateToTicket[vehicle->plate];
        auto ticket = activeTickets[tid];

        int minutes = (time(nullptr) - ticket->entry)/ 60;

        auto floor = floors[ticket->floor];
        lock_guard<mutex> lock(floor->mtx);

        for(auto spot: floor->spots) {
            if(spot->id == ticket->spotid) {
                spot->free = true;
                floor->freeCount[spot->type]++;
                break;
            }
        }

        double amount = pricing->fare(vehicle->type, minutes);
        cout<<"Payment: "<< amount<< "\n";

        activeTickets.erase(tid);
        plateToTicket.erase(vehicle->plate);
        return true;
    }

       // ----- Real-Time Availability -----
    void printAvailability() {
        cout << "==== Availability ====\n";
        for(auto f : floors) {
            lock_guard<mutex> lock(f->mtx);

            cout << "Floor " << f->id 
                 << " | Small="  << f->freeCount[SpotType::Small]
                 << " Medium="   << f->freeCount[SpotType::Medium]
                 << " Large="    << f->freeCount[SpotType::Large]
                 << "\n";
        }
    }
};

struct EntryGate {
    string id;
    ParkingLot& lot;
    EntryGate(string i, ParkingLot& lot): id(i), lot(lot) {}

    string enter(shared_ptr<Vehicle> v) {
        string t = lot.park(v);
        cout<<"["<<id<<"] "<<v->plate<<" -> "<<(t==""?"NO SPOT":t)<<"\n";
        return t;
    }
};

struct ExitGate {
    string id;
    ParkingLot& lot;
    ExitGate(string i, ParkingLot& lot): id(i), lot(lot) {}

    void leave(shared_ptr<Vehicle> v) {
        bool ok = lot.unpark(v);
        cout<<"["<<id<<"] "<<v->plate<<" exit -> "<<(ok?"OK":"FAIL")<<"\n";
    } 
};

int main() {
    SimpleHour pricing;
    ParkingLot lot(&pricing);

    auto f1 = make_shared<ParkingFloor>(0);
    f1->addSpots(SpotType::Small,  3);
    f1->addSpots(SpotType::Medium, 3);
    f1->addSpots(SpotType::Large,  2);

    EntryGate E1("Gate-1", lot);
    EntryGate E2("Gate-2", lot);
    ExitGate  X1("Exit-1", lot);

    lot.addFloor(f1);

    vector<shared_ptr<Vehicle>> vehicles = {
        std::make_shared<CarVehicle>("A111"),
        std::make_shared<BikeVehicle>("B222"),
        std::make_shared<TruckVehicle>("C333"),
        std::make_shared<CarVehicle>("D444"),
        std::make_shared<BikeVehicle>("E555")
    };

    vector<thread> threads;

    for(auto &v: vehicles) {
        threads.emplace_back([&](){
            E1.enter(v);
        });
    }

    this_thread::sleep_for(chrono::milliseconds(500));
    threads.emplace_back([&](){X1.leave(vehicles[0]);});
    threads.emplace_back([&](){X1.leave(vehicles[1]);});

    for(auto &t: threads) t.join();
    lot.printAvailability();
}