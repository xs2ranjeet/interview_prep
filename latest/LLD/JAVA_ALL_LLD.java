// ============================================================================
// 1. PARKING LOT SYSTEM
// ============================================================================

// Enums
enum VehicleType {
    BIKE, CAR, TRUCK, BUS
}

enum ParkingSpotType {
    BIKE, COMPACT, LARGE, HANDICAPPED
}

enum ParkingTicketStatus {
    ACTIVE, PAID, LOST
}

// Vehicle Classes
abstract class Vehicle {
    private String licensePlate;
    private VehicleType type;
    
    public Vehicle(String licensePlate, VehicleType type) {
        this.licensePlate = licensePlate;
        this.type = type;
    }
    
    public String getLicensePlate() { return licensePlate; }
    public VehicleType getType() { return type; }
}

class Bike extends Vehicle {
    public Bike(String licensePlate) {
        super(licensePlate, VehicleType.BIKE);
    }
}

class Car extends Vehicle {
    public Car(String licensePlate) {
        super(licensePlate, VehicleType.CAR);
    }
}

class Truck extends Vehicle {
    public Truck(String licensePlate) {
        super(licensePlate, VehicleType.TRUCK);
    }
}

// Parking Spot
class ParkingSpot {
    private String spotId;
    private ParkingSpotType type;
    private boolean isAvailable;
    private Vehicle vehicle;
    private int floor;
    
    public ParkingSpot(String spotId, ParkingSpotType type, int floor) {
        this.spotId = spotId;
        this.type = type;
        this.floor = floor;
        this.isAvailable = true;
    }
    
    public boolean canFitVehicle(Vehicle vehicle) {
        switch (vehicle.getType()) {
            case BIKE:
                return type == ParkingSpotType.BIKE;
            case CAR:
                return type == ParkingSpotType.COMPACT || 
                       type == ParkingSpotType.LARGE || 
                       type == ParkingSpotType.HANDICAPPED;
            case TRUCK:
            case BUS:
                return type == ParkingSpotType.LARGE;
            default:
                return false;
        }
    }
    
    public void parkVehicle(Vehicle vehicle) {
        this.vehicle = vehicle;
        this.isAvailable = false;
    }
    
    public void removeVehicle() {
        this.vehicle = null;
        this.isAvailable = true;
    }
    
    public boolean isAvailable() { return isAvailable; }
    public String getSpotId() { return spotId; }
    public ParkingSpotType getType() { return type; }
    public int getFloor() { return floor; }
}

// Parking Ticket
class ParkingTicket {
    private String ticketId;
    private String licensePlate;
    private ParkingSpot spot;
    private long entryTime;
    private long exitTime;
    private double amount;
    private ParkingTicketStatus status;
    
    public ParkingTicket(String ticketId, String licensePlate, ParkingSpot spot) {
        this.ticketId = ticketId;
        this.licensePlate = licensePlate;
        this.spot = spot;
        this.entryTime = System.currentTimeMillis();
        this.status = ParkingTicketStatus.ACTIVE;
    }
    
    public void setExitTime(long exitTime) { this.exitTime = exitTime; }
    public void setAmount(double amount) { this.amount = amount; }
    public void setStatus(ParkingTicketStatus status) { this.status = status; }
    
    public String getTicketId() { return ticketId; }
    public ParkingSpot getSpot() { return spot; }
    public long getEntryTime() { return entryTime; }
    public long getExitTime() { return exitTime; }
    public double getAmount() { return amount; }
    public ParkingTicketStatus getStatus() { return status; }
}

// Payment Strategy
interface PaymentStrategy {
    boolean processPayment(double amount);
}

class CashPayment implements PaymentStrategy {
    @Override
    public boolean processPayment(double amount) {
        System.out.println("Processing cash payment: $" + amount);
        return true;
    }
}

class CardPayment implements PaymentStrategy {
    private String cardNumber;
    
    public CardPayment(String cardNumber) {
        this.cardNumber = cardNumber;
    }
    
    @Override
    public boolean processPayment(double amount) {
        System.out.println("Processing card payment: $" + amount);
        return true;
    }
}

// Parking Rate Strategy
interface ParkingRateStrategy {
    double calculateFee(long durationMillis, ParkingSpotType spotType);
}

class HourlyRateStrategy implements ParkingRateStrategy {
    private static final double BIKE_RATE = 2.0;
    private static final double COMPACT_RATE = 5.0;
    private static final double LARGE_RATE = 10.0;
    
    @Override
    public double calculateFee(long durationMillis, ParkingSpotType spotType) {
        long hours = (durationMillis / (1000 * 60 * 60)) + 1; // Ceiling
        
        switch (spotType) {
            case BIKE:
                return hours * BIKE_RATE;
            case COMPACT:
            case HANDICAPPED:
                return hours * COMPACT_RATE;
            case LARGE:
                return hours * LARGE_RATE;
            default:
                return 0.0;
        }
    }
}

// Parking Floor
class ParkingFloor {
    private int floorNumber;
    private List<ParkingSpot> spots;
    
    public ParkingFloor(int floorNumber) {
        this.floorNumber = floorNumber;
        this.spots = new ArrayList<>();
    }
    
    public void addSpot(ParkingSpot spot) {
        spots.add(spot);
    }
    
    public ParkingSpot findAvailableSpot(Vehicle vehicle) {
        for (ParkingSpot spot : spots) {
            if (spot.isAvailable() && spot.canFitVehicle(vehicle)) {
                return spot;
            }
        }
        return null;
    }
    
    public int getAvailableSpotCount(ParkingSpotType type) {
        return (int) spots.stream()
            .filter(s -> s.isAvailable() && s.getType() == type)
            .count();
    }
}

// Main Parking Lot System
class ParkingLot {
    private static ParkingLot instance;
    private String name;
    private List<ParkingFloor> floors;
    private Map<String, ParkingTicket> activeTickets;
    private ParkingRateStrategy rateStrategy;
    
    private ParkingLot(String name) {
        this.name = name;
        this.floors = new ArrayList<>();
        this.activeTickets = new HashMap<>();
        this.rateStrategy = new HourlyRateStrategy();
    }
    
    public static synchronized ParkingLot getInstance(String name) {
        if (instance == null) {
            instance = new ParkingLot(name);
        }
        return instance;
    }
    
    public void addFloor(ParkingFloor floor) {
        floors.add(floor);
    }
    
    public ParkingTicket parkVehicle(Vehicle vehicle) {
        ParkingSpot spot = findAvailableSpot(vehicle);
        
        if (spot == null) {
            System.out.println("No available spot for vehicle: " + vehicle.getLicensePlate());
            return null;
        }
        
        spot.parkVehicle(vehicle);
        String ticketId = generateTicketId();
        ParkingTicket ticket = new ParkingTicket(ticketId, vehicle.getLicensePlate(), spot);
        activeTickets.put(ticketId, ticket);
        
        System.out.println("Vehicle parked at spot: " + spot.getSpotId());
        return ticket;
    }
    
    public boolean unparkVehicle(String ticketId, PaymentStrategy paymentStrategy) {
        ParkingTicket ticket = activeTickets.get(ticketId);
        
        if (ticket == null) {
            System.out.println("Invalid ticket ID");
            return false;
        }
        
        ticket.setExitTime(System.currentTimeMillis());
        long duration = ticket.getExitTime() - ticket.getEntryTime();
        double amount = rateStrategy.calculateFee(duration, ticket.getSpot().getType());
        ticket.setAmount(amount);
        
        if (paymentStrategy.processPayment(amount)) {
            ticket.setStatus(ParkingTicketStatus.PAID);
            ticket.getSpot().removeVehicle();
            activeTickets.remove(ticketId);
            System.out.println("Vehicle unparked successfully. Fee: $" + amount);
            return true;
        }
        
        return false;
    }
    
    private ParkingSpot findAvailableSpot(Vehicle vehicle) {
        for (ParkingFloor floor : floors) {
            ParkingSpot spot = floor.findAvailableSpot(vehicle);
            if (spot != null) {
                return spot;
            }
        }
        return null;
    }
    
    private String generateTicketId() {
        return "TKT" + System.currentTimeMillis();
    }
    
    public void displayAvailability() {
        System.out.println("\n=== Parking Availability ===");
        for (int i = 0; i < floors.size(); i++) {
            ParkingFloor floor = floors.get(i);
            System.out.println("Floor " + i + ":");
            System.out.println("  BIKE: " + floor.getAvailableSpotCount(ParkingSpotType.BIKE));
            System.out.println("  COMPACT: " + floor.getAvailableSpotCount(ParkingSpotType.COMPACT));
            System.out.println("  LARGE: " + floor.getAvailableSpotCount(ParkingSpotType.LARGE));
        }
    }
}


// ============================================================================
// 2. SNAKE AND LADDER GAME
// ============================================================================

// Player
class Player {
    private String name;
    private int position;
    
    public Player(String name) {
        this.name = name;
        this.position = 0;
    }
    
    public String getName() { return name; }
    public int getPosition() { return position; }
    public void setPosition(int position) { this.position = position; }
}

// Dice
class Dice {
    private int numDice;
    private Random random;
    
    public Dice(int numDice) {
        this.numDice = numDice;
        this.random = new Random();
    }
    
    public int roll() {
        int total = 0;
        for (int i = 0; i < numDice; i++) {
            total += random.nextInt(6) + 1; // 1 to 6
        }
        System.out.println("Dice rolled: " + total);
        return total;
    }
}

// Cell (can be normal, snake head, or ladder bottom)
abstract class Cell {
    protected int position;
    
    public Cell(int position) {
        this.position = position;
    }
    
    public int getPosition() { return position; }
    public abstract int getNextPosition(int currentPosition);
}

class NormalCell extends Cell {
    public NormalCell(int position) {
        super(position);
    }
    
    @Override
    public int getNextPosition(int currentPosition) {
        return currentPosition;
    }
}

class Snake extends Cell {
    private int tail;
    
    public Snake(int head, int tail) {
        super(head);
        this.tail = tail;
    }
    
    @Override
    public int getNextPosition(int currentPosition) {
        System.out.println("Snake bite! Moving from " + currentPosition + " to " + tail);
        return tail;
    }
}

class Ladder extends Cell {
    private int top;
    
    public Ladder(int bottom, int top) {
        super(bottom);
        this.top = top;
    }
    
    @Override
    public int getNextPosition(int currentPosition) {
        System.out.println("Ladder climb! Moving from " + currentPosition + " to " + top);
        return top;
    }
}

// Board
class Board {
    private int size;
    private Cell[] cells;
    
    public Board(int size) {
        this.size = size;
        this.cells = new Cell[size + 1];
        
        // Initialize all cells as normal
        for (int i = 0; i <= size; i++) {
            cells[i] = new NormalCell(i);
        }
    }
    
    public void addSnake(int head, int tail) {
        if (head > tail && head <= size && tail >= 0) {
            cells[head] = new Snake(head, tail);
        }
    }
    
    public void addLadder(int bottom, int top) {
        if (top > bottom && top <= size && bottom >= 0) {
            cells[bottom] = new Ladder(bottom, top);
        }
    }
    
    public int getNextPosition(int position) {
        if (position > size) return position;
        return cells[position].getNextPosition(position);
    }
    
    public int getSize() { return size; }
}

// Game
class SnakeAndLadderGame {
    private Board board;
    private Dice dice;
    private Queue<Player> players;
    private int winningPosition;
    
    public SnakeAndLadderGame(int boardSize, int numDice) {
        this.board = new Board(boardSize);
        this.dice = new Dice(numDice);
        this.players = new LinkedList<>();
        this.winningPosition = boardSize;
    }
    
    public void addPlayer(Player player) {
        players.add(player);
    }
    
    public void addSnake(int head, int tail) {
        board.addSnake(head, tail);
    }
    
    public void addLadder(int bottom, int top) {
        board.addLadder(bottom, top);
    }
    
    public void start() {
        System.out.println("\n=== Game Started ===\n");
        
        while (players.size() > 1) {
            Player currentPlayer = players.poll();
            System.out.println("\n" + currentPlayer.getName() + "'s turn (Position: " + 
                             currentPlayer.getPosition() + ")");
            
            int diceValue = dice.roll();
            int newPosition = currentPlayer.getPosition() + diceValue;
            
            // Can't move beyond winning position
            if (newPosition > winningPosition) {
                System.out.println("Can't move! Need exact roll to win.");
                players.add(currentPlayer);
                continue;
            }
            
            // Check for snake or ladder
            newPosition = board.getNextPosition(newPosition);
            currentPlayer.setPosition(newPosition);
            
            System.out.println(currentPlayer.getName() + " moved to position: " + newPosition);
            
            // Check if player won
            if (newPosition == winningPosition) {
                System.out.println("\n*** " + currentPlayer.getName() + " WINS! ***\n");
                break;
            }
            
            players.add(currentPlayer);
        }
    }
}


// ============================================================================
// 3. VENDING MACHINE
// ============================================================================

// Product
class Product {
    private String code;
    private String name;
    private double price;
    
    public Product(String code, String name, double price) {
        this.code = code;
        this.name = name;
        this.price = price;
    }
    
    public String getCode() { return code; }
    public String getName() { return name; }
    public double getPrice() { return price; }
}

// Inventory Item
class InventoryItem {
    private Product product;
    private int quantity;
    
    public InventoryItem(Product product, int quantity) {
        this.product = product;
        this.quantity = quantity;
    }
    
    public Product getProduct() { return product; }
    public int getQuantity() { return quantity; }
    
    public void decreaseQuantity() {
        if (quantity > 0) quantity--;
    }
    
    public void increaseQuantity(int count) {
        quantity += count;
    }
    
    public boolean isAvailable() {
        return quantity > 0;
    }
}

// Inventory
class Inventory {
    private Map<String, InventoryItem> items;
    
    public Inventory() {
        this.items = new HashMap<>();
    }
    
    public void addProduct(Product product, int quantity) {
        items.put(product.getCode(), new InventoryItem(product, quantity));
    }
    
    public InventoryItem getItem(String productCode) {
        return items.get(productCode);
    }
    
    public boolean isAvailable(String productCode) {
        InventoryItem item = items.get(productCode);
        return item != null && item.isAvailable();
    }
    
    public void updateQuantity(String productCode, int quantity) {
        InventoryItem item = items.get(productCode);
        if (item != null) {
            item.increaseQuantity(quantity);
        }
    }
    
    public void displayInventory() {
        System.out.println("\n=== Available Products ===");
        for (Map.Entry<String, InventoryItem> entry : items.entrySet()) {
            InventoryItem item = entry.getValue();
            Product product = item.getProduct();
            System.out.println(product.getCode() + ": " + product.getName() + 
                             " - $" + product.getPrice() + 
                             " (Qty: " + item.getQuantity() + ")");
        }
        System.out.println();
    }
}

// Coin/Note
enum Coin {
    PENNY(0.01),
    NICKEL(0.05),
    DIME(0.10),
    QUARTER(0.25),
    DOLLAR(1.00);
    
    private double value;
    
    Coin(double value) {
        this.value = value;
    }
    
    public double getValue() { return value; }
}

// Vending Machine States
interface VendingMachineState {
    void insertMoney(VendingMachine machine, double amount);
    void selectProduct(VendingMachine machine, String productCode);
    void dispenseProduct(VendingMachine machine);
    void returnMoney(VendingMachine machine);
}

class IdleState implements VendingMachineState {
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        machine.addMoney(amount);
        System.out.println("Money inserted: $" + amount);
        System.out.println("Total: $" + machine.getCurrentAmount());
        machine.setState(machine.getHasMoneyState());
    }
    
    @Override
    public void selectProduct(VendingMachine machine, String productCode) {
        System.out.println("Please insert money first");
    }
    
    @Override
    public void dispenseProduct(VendingMachine machine) {
        System.out.println("Please insert money and select product");
    }
    
    @Override
    public void returnMoney(VendingMachine machine) {
        System.out.println("No money to return");
    }
}

class HasMoneyState implements VendingMachineState {
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        machine.addMoney(amount);
        System.out.println("Money inserted: $" + amount);
        System.out.println("Total: $" + machine.getCurrentAmount());
    }
    
    @Override
    public void selectProduct(VendingMachine machine, String productCode) {
        Inventory inventory = machine.getInventory();
        
        if (!inventory.isAvailable(productCode)) {
            System.out.println("Product not available");
            return;
        }
        
        InventoryItem item = inventory.getItem(productCode);
        Product product = item.getProduct();
        
        if (machine.getCurrentAmount() < product.getPrice()) {
            System.out.println("Insufficient money. Need $" + 
                             (product.getPrice() - machine.getCurrentAmount()) + " more");
            return;
        }
        
        machine.setSelectedProduct(product);
        machine.setState(machine.getDispenseState());
        dispenseProduct(machine);
    }
    
    @Override
    public void dispenseProduct(VendingMachine machine) {
        System.out.println("Please select a product first");
    }
    
    @Override
    public void returnMoney(VendingMachine machine) {
        System.out.println("Returning money: $" + machine.getCurrentAmount());
        machine.setCurrentAmount(0);
        machine.setState(machine.getIdleState());
    }
}

class DispenseState implements VendingMachineState {
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        System.out.println("Please wait, dispensing product");
    }
    
    @Override
    public void selectProduct(VendingMachine machine, String productCode) {
        System.out.println("Product already selected");
    }
    
    @Override
    public void dispenseProduct(VendingMachine machine) {
        Product product = machine.getSelectedProduct();
        Inventory inventory = machine.getInventory();
        
        System.out.println("\nDispensing: " + product.getName());
        
        // Update inventory
        InventoryItem item = inventory.getItem(product.getCode());
        item.decreaseQuantity();
        
        // Calculate change
        double change = machine.getCurrentAmount() - product.getPrice();
        if (change > 0) {
            System.out.println("Returning change: $" + String.format("%.2f", change));
        }
        
        // Reset machine
        machine.setCurrentAmount(0);
        machine.setSelectedProduct(null);
        machine.setState(machine.getIdleState());
        
        System.out.println("Thank you for your purchase!\n");
    }
    
    @Override
    public void returnMoney(VendingMachine machine) {
        System.out.println("Cannot return money while dispensing");
    }
}

// Vending Machine (Context)
class VendingMachine {
    private VendingMachineState idleState;
    private VendingMachineState hasMoneyState;
    private VendingMachineState dispenseState;
    
    private VendingMachineState currentState;
    private Inventory inventory;
    private double currentAmount;
    private Product selectedProduct;
    
    public VendingMachine() {
        this.idleState = new IdleState();
        this.hasMoneyState = new HasMoneyState();
        this.dispenseState = new DispenseState();
        
        this.currentState = idleState;
        this.inventory = new Inventory();
        this.currentAmount = 0.0;
    }
    
    public void addProduct(Product product, int quantity) {
        inventory.addProduct(product, quantity);
    }
    
    public void insertMoney(double amount) {
        currentState.insertMoney(this, amount);
    }
    
    public void selectProduct(String productCode) {
        currentState.selectProduct(this, productCode);
    }
    
    public void dispenseProduct() {
        currentState.dispenseProduct(this);
    }
    
    public void returnMoney() {
        currentState.returnMoney(this);
    }
    
    public void displayProducts() {
        inventory.displayInventory();
    }
    
    // Getters and setters
    public void setState(VendingMachineState state) { this.currentState = state; }
    public void addMoney(double amount) { this.currentAmount += amount; }
    public void setCurrentAmount(double amount) { this.currentAmount = amount; }
    public void setSelectedProduct(Product product) { this.selectedProduct = product; }
    
    public VendingMachineState getIdleState() { return idleState; }
    public VendingMachineState getHasMoneyState() { return hasMoneyState; }
    public VendingMachineState getDispenseState() { return dispenseState; }
    public Inventory getInventory() { return inventory; }
    public double getCurrentAmount() { return currentAmount; }
    public Product getSelectedProduct() { return selectedProduct; }
}


// ============================================================================
// DEMO / MAIN
// ============================================================================

class LLDDemo {
    public static void main(String[] args) {
        // Demo 1: Parking Lot
        demoParkingLot();
        
        // Demo 2: Snake and Ladder
        demoSnakeAndLadder();
        
        // Demo 3: Vending Machine
        demoVendingMachine();
    }
    
    private static void demoParkingLot() {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("PARKING LOT SYSTEM DEMO");
        System.out.println("=".repeat(60));
        
        ParkingLot parkingLot = ParkingLot.getInstance("Mall Parking");
        
        // Create floors and spots
        ParkingFloor floor1 = new ParkingFloor(1);
        floor1.addSpot(new ParkingSpot("F1-B1", ParkingSpotType.BIKE, 1));
        floor1.addSpot(new ParkingSpot("F1-B2", ParkingSpotType.BIKE, 1));
        floor1.addSpot(new ParkingSpot("F1-C1", ParkingSpotType.COMPACT, 1));
        floor1.addSpot(new ParkingSpot("F1-C2", ParkingSpotType.COMPACT, 1));
        floor1.addSpot(new ParkingSpot("F1-L1", ParkingSpotType.LARGE, 1));
        
        parkingLot.addFloor(floor1);
        parkingLot.displayAvailability();
        
        // Park vehicles
        Vehicle bike = new Bike("BIKE-123");
        Vehicle car = new Car("CAR-456");
        Vehicle truck = new Truck("TRUCK-789");
        
        ParkingTicket ticket1 = parkingLot.parkVehicle(bike);
        ParkingTicket ticket2 = parkingLot.parkVehicle(car);
        ParkingTicket ticket3 = parkingLot.parkVehicle(truck);
        
        parkingLot.displayAvailability();
        
        // Unpark a vehicle
        System.out.println("\n--- Unparking car ---");
        parkingLot.unparkVehicle(ticket2.getTicketId(), new CardPayment("1234-5678"));
        
        parkingLot.displayAvailability();
    }
    
    private static void demoSnakeAndLadder() {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("SNAKE AND LADDER GAME DEMO");
        System.out.println("=".repeat(60));
        
        SnakeAndLadderGame game = new SnakeAndLadderGame(100, 1);
        
        // Add players
        game.addPlayer(new Player("Alice"));
        game.addPlayer(new Player("Bob"));
        
        // Add snakes
        game.addSnake(99, 54);
        game.addSnake(70, 55);
        game.addSnake(52, 42);
        game.addSnake(25, 2);
        
        // Add ladders
        game.addLadder(6, 25);
        game.addLadder(11, 40);
        game.addLadder(60, 85);
        game.addLadder(46, 90);
        
        game.start();
    }
    
    private static void demoVendingMachine() {
        System.out.println("\n" + "=".repeat(60));
        System.out.println("VENDING MACHINE DEMO");
        System.out.println("=".repeat(60));
        
        VendingMachine machine = new VendingMachine();
        
        // Add products
        machine.addProduct(new Product("A1", "Coke", 1.50), 10);
        machine.addProduct(new Product("A2", "Pepsi", 1.50), 8);
        machine.addProduct(new Product("B1", "Water", 1.00), 15);
        machine.addProduct(new Product("B2", "Juice", 2.00), 5);
        machine.addProduct(new Product("C1", "Chips", 1.25), 12);
        
        machine.displayProducts();
        
        // Simulate purchase
        System.out.println("--- Transaction 1: Buying Coke ---");
        machine.insertMoney(1.00);
        machine.insertMoney(0.50);
        machine.selectProduct("A1");
        
        machine.displayProducts();
        
        System.out.println("\n--- Transaction 2: Buying Juice with change ---");
        machine.insertMoney(2.00);
        machine.insertMoney(0.50);
        machine.selectProduct("B2");
        
        System.out.println("\n--- Transaction 3: Return money ---");
        machine.insertMoney(1.00);
        machine.returnMoney();
    }
}

import java.util.*;