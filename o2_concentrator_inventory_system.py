import sys

class Concentrator:
    def __init__(self, model, rma, revenue, flow_rate, is_repaired):
        self._model = model
        self._rma = rma
        self._revenue = float(revenue.strip("$"))
        self._flow_rate = flow_rate
        self._is_repaired = is_repaired
            
    @property
    def is_repaired(self):
        return self._is_repaired
    
    @is_repaired.setter
    def is_repaired(self, value):
        self._is_repaired = value
    
    def get_info(self):
        return f"Model: {self._model} - RMA: {self._rma} | Revenue: ${self._revenue} | Flow Rate: {self._flow_rate}L | Repaired: {self._is_repaired}"
        
    def __str__(self):
        return self.get_info()
    

class HomeConcentrator(Concentrator):
    def __init__(self, model, rma, revenue, flow_rate, is_repaired, noise_level):
        super().__init__(model, rma, revenue, flow_rate, is_repaired)
        self._noise_level = float(noise_level)
        
    def get_info(self):
        return super().get_info() + f" | Noise level: {self._noise_level} dB"

class PortableConcentrator(Concentrator):
    def __init__(self, model, rma, revenue, flow_rate, is_repaired, battery_level):
        super().__init__(model, rma, revenue, flow_rate, is_repaired)
        self._battery_level = battery_level
    
    def get_info(self):
        return super().get_info() + f" | Battery level: {self._battery_level}%"
    
class PediatricConcentrator(Concentrator):
    def __init__(self, model, rma, revenue, flow_rate, is_repaired, age):
        super().__init__(model, rma, revenue, flow_rate, is_repaired)
        self._age = age
        
    def get_info(self):
        return super().get_info() + f" | Age: {self._age}"
    
class Inventory:
    def __init__(self):
        self._stock = []
    
    def receive_unit(self, unit):
        if any(u._rma == unit._rma for u in self._stock):
            print(f"\nRMA {unit._rma} already exists! Unit not added.\n")
        else:
            self._stock.append(unit)
        
    def ship_unit(self, unit):
        if unit in self._stock:
            self._stock.remove(unit)
        else:
            print("\nUnit not found!\n")
            
    def check_repair_status(self, rma):
        unit = next((u for u in self._stock if u._rma == rma), None)
        return unit._is_repaired if unit else None
        
    def show_stock(self):
        if not self._stock:
            return "No units in inventory"
        else:
            return "\n".join([str(unit) for unit in self._stock])
        
    def show_revenue(self):
        return f"Total Revenue value: ${sum(unit._revenue for unit in self._stock):.2f}"
    

def main():
    inv = Inventory()
    while True:
        selection = input("Enter selection: \n1.Receive unit\n2.Ship unit\n3.Check repair status\n4.View inventory\n5.Show revenue\n6.Exit\n")
        if selection == "1":
            receiving(inv)
        elif selection == "2":
            shipping(inv)
        elif selection == "3":
            rma = input("Enter RMA to check repair status: ").strip().upper()
            status = inv.check_repair_status(rma)
            if status is not None:
                print(f"Repair status: {status}")
            else:
                print("\nUnit not found!\n")
        elif selection == "4":
            print(f"\n{inv.show_stock()}\n")
        elif selection == "5":
            print(f"\n{inv.show_revenue()}\n")
        elif selection == "6":
            sys.exit("-------------------------------------------------------\nThank you for using my O2 Inventory management system!\n-------------------------------------------------------")
        else:
            print("Invalid input!")

            



def receiving(inv):
    keep_receiving = True
    while keep_receiving:
        type = input("Enter type of unit to receive: \n1.Home\n2.Portable\n3.Pediatric\n4.Exit\n")
        
        if type == "1":
            model, rma, revenue, flow_rate, is_repaired = receive()  
            noise_level = input("Enter noise level in dB: ")
            unit = HomeConcentrator(model, rma, revenue, flow_rate, is_repaired, noise_level)
            inv.receive_unit(unit)
            print(f"\nUnit received\n")

        elif type == "2":
            model, rma, revenue, flow_rate, is_repaired = receive()
            battery_level = input("Enter battery level: ")
            unit = PortableConcentrator(model, rma, revenue, flow_rate, is_repaired, battery_level)
            inv.receive_unit(unit)
            print(f"\nUnit received\n")

        elif type == "3":
            model, rma, revenue, flow_rate, is_repaired = receive()
            age = input("Enter patients age: ")
            unit = PediatricConcentrator(model, rma, revenue, flow_rate, is_repaired, age)
            inv.receive_unit(unit)
            print(f"\nUnit received\n")
        
        elif type == "4":
            break

        else:
            print("Invalid Input")

        
def receive():
    model = input("Enter Model type: ")
    rma = input("Enter RMA: ").strip().upper()
    revenue = input("Enter revenue amount: ")
    flow_rate = float(input("Enter Flow Rate in liters: "))
    repaired = True
    while repaired:
        is_repaired = input("Is the unit repaired(y/n): ").lower()
        if is_repaired == "y":
            is_repaired = "Yes"
            repaired = False
        elif is_repaired == "n":
            is_repaired = "No"
            repaired = False
        else:
            print("Incorrect input")

    return model, rma, revenue, flow_rate, is_repaired
            

def shipping(inv):
    keep_shipping = True
    while keep_shipping:
        if not inv._stock:
            print("\nNo units available to ship.\n")
            break
        print("\nCurrent Inventory: \n")
        print(f"\n{inv.show_stock()}\n")
        rma = input("\nEnter RMA of unit to ship or c to cancel: \n").strip().upper()
        if rma.lower() == "c":
            break
        unit = next((u for u in inv._stock if u._rma == rma), None)
        if unit:
            inv.ship_unit(unit)
            print(f"\nUnit with RMA {rma} has been shipped!\n")
        else:
            print(f"\nUnit with RMA {rma} not found\n")
           
    
    
if __name__ == "__main__":
    main()


#Objectives
'''
-...
'''
