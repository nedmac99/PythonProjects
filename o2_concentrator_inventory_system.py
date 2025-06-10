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
        return f"Model: {self._model} - RMA: {self._rma} | Revenue: {self._revenue} | Flow Rate: {self._flow_rate} | Repaired: {self._is_repaired}"
        
    def __str__(self):
        return self.get_info()
    

class HomeConcentrator(Concentrator):
    def __init__(self, model, rma, revenue, flow_rate, is_repaired, noise_level):
        super().__init__(model, rma, revenue, flow_rate, is_repaired)
        self._noise_level = noise_level
        
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
        self._stock.append(unit)
        
    def ship_unit(self, unit):
        if unit in self._stock:
            self._stock.remove(unit)
        else:
            print("Unit not found!")
            
    def check_repair_status(self, unit):
        return unit._is_repaired
        
    def show_stock(self):
        if not self._stock:
            return "No units in inventory"
        else:
            return "\n".join([str(unit) for unit in self._stock])
        
    def show_revenue(self):
        return f"Total Revenue value: ${sum(unit._revenue for unit in self._stock):.2f}"
    

def main():
    type = input("Enter type: \n1.Home\n2.Portable\n3.Pediatric\n")
    
    if type == "1":
        model = input("Enter Model type: ")
        rma = input("Enter RMA: ")
        revenue = input("Enter revenue amount: ")
        flow_rate = input("Enter Flow Rate in liters: ")
        is_repaired = input("Is the unit repaired(y/n): ")
        noise_level = input("Enter noise level in dB: ")
        unit = HomeConcentrator(model, rma, revenue, flow_rate, is_repaired, noise_level)
        ######Continue Here#####
        
    elif type == "2":
        model = input("Enter Model type: ")
        rma = input("Enter RMA: ")
        revenue = input("Enter revenue amount: ")
        flow_rate = input("Enter Flow Rate in liters: ")
        is_repaired = input("Is the unit repaired(y/n): ")
    elif type == "3":
        model = input("Enter Model type: ")
        rma = input("Enter RMA: ")
        revenue = input("Enter revenue amount: ")
        flow_rate = input("Enter Flow Rate in liters: ")
        is_repaired = input("Is the unit repaired(y/n): ")
    else:
        print("Invalid Input")
    
    
    
    
if __name__ == "__main__":
    main()