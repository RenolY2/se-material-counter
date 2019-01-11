valid_resources = [
"largetube", "smalltube", "motor", "steelplate", "solarcell",
"constcomp", "interiorplate", "display", "girder",
"metalgrid", "powercell", "glass", "computer", "medcomp",
"reactorcomp"]

valid_raw_mats = ["ironingot", "cobaltingot", "nickelingot", "siliconwafer", "silveringot"]


class MaterialProperty(object):
    def __init__(self, weight, volume):
        self.weight = weight 
        self.volume = volume 
    
    def __add__(self, other):
        return MaterialProperty(self.weight+other.weight, self.volume+other.volume)
    
    def __mul__(self, other):
        return MaterialProperty(self.weight*other, self.volume*other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __str__(self):
        return "Weight: {0}kg; Volume: {1}".format(self.weight, self.volume) 

        
class ResourceRequirement(object):
    def __init__(self, **kwargs):
        assert all(x in valid_resources for x in kwargs.keys())
        
        self.req = {}
        for resource in valid_resources:
            self.req[resource] = 0
            
        for resource, count in kwargs.items():
            assert isinstance(count, int)
            
            self.req[resource] = count 
    
    def __add__(self, other):
        new_req = ResourceRequirement()
        
        for resource, count in self.req.items():
            new_req.req[resource] += count 
        
        for resource, count in other.req.items():
            new_req.req[resource] += count 
        
        return new_req 
    
    def __mul__(self, other):
        new_req = ResourceRequirement()
        
        for resource, count in self.req.items():
            new_req.req[resource] += other*count 
        
        return new_req 
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __str__(self):
        prettified = {}
        
        for resource, count in self.req.items():
            if count > 0:
                prettified[resource] = count 
        
        return str(prettified)
        
class AssemblyRequirement(ResourceRequirement):
    def __init__(self, **kwargs):
        assert all(x in valid_raw_mats for x in kwargs.keys())
        
        self.req = {}
        for resource in valid_raw_mats:
            self.req[resource] = 0
            
        for resource, count in kwargs.items():
            assert isinstance(count, (int, float))
            
            self.req[resource] = count 
            
    def __add__(self, other):
        new_req = AssemblyRequirement()
        
        for resource, count in self.req.items():
            new_req.req[resource] += count 
        
        for resource, count in other.req.items():
            new_req.req[resource] += count 
        
        return new_req 
    
    def __mul__(self, other):
        new_req = AssemblyRequirement()
        
        for resource, count in self.req.items():
            new_req.req[resource] += other*count 
        
        return new_req 

matproperties = {
    "largetube": (MaterialProperty(25.0, 38.0), AssemblyRequirement(ironingot=30.0)),
    "smalltube": (MaterialProperty(4.0, 2.0), AssemblyRequirement(ironingot=5.0)),
    "steelplate": (MaterialProperty(20.0, 3.0), AssemblyRequirement(ironingot=21.0)),
    "constcomp": (MaterialProperty(8.0, 2.0), AssemblyRequirement(ironingot=10.0)),
    "interiorplate": (MaterialProperty(3.0, 5.0), AssemblyRequirement(ironingot=3.5)),
    "metalgrid": (MaterialProperty(6.0, 15.0), AssemblyRequirement(ironingot=12.0, nickelingot=5.0, cobaltingot=3.0)),
    
    "motor": (MaterialProperty(24.0, 8.0), AssemblyRequirement(ironingot=20.0, nickelingot=5.0)),
    "solarcell": (MaterialProperty(8.0, 20.0), AssemblyRequirement(nickelingot=10.0, siliconwafer=8.0)),
    "powercell": (MaterialProperty(25.0, 45.0), AssemblyRequirement(ironingot=10.0, nickelingot=2.0, siliconwafer=1.0)),
    
    "display": (MaterialProperty(8.0, 6.0), AssemblyRequirement(ironingot=1.0, siliconwafer=5.0)),
    "computer": (MaterialProperty(0.2, 1.0), AssemblyRequirement(ironingot=0.5, siliconwafer=0.2)),
    
    "medcomp": (MaterialProperty(150.0, 160.0), AssemblyRequirement(ironingot=60.0, nickelingot=70.0, silveringot=20.0)),
    
    
    "ironingot": (MaterialProperty(1.0, 0.127), None),
    "nickelingot": (MaterialProperty(1.0, 0.112), None),
    "cobaltingot": (MaterialProperty(1.0, 0.112), None),
    "siliconwafer": (MaterialProperty(1, 0.429), None),
    "silveringot": (MaterialProperty(1.0, 0.095), None)

}    

def calculate_weight_and_vol(res):
    weight = 0.0
    volume = 0.0
    
    for resource, count in res.req.items():
        if count == 0: continue 
        
        matprop, _ = matproperties[resource]
        
        weight += matprop.weight * count 
        volume += matprop.volume * count 
    
    return MaterialProperty(weight, volume)

def calculate_raw_mats(res):
    raw_req = AssemblyRequirement()
    
    for resource, count in res.req.items():
        if count == 0: continue 
        _, asmreq = matproperties[resource]
        raw_req = raw_req + asmreq*count 
    
    return raw_req 
    
LightArmor = ResourceRequirement(steelplate = 25)
ConveyorJunction = ResourceRequirement( interiorplate=20, constcomp=30, 
                                        smalltube=20, motor=6)
ConveyorTube = ResourceRequirement( interiorplate=14, motor=6, 
                                    smalltube=12, constcomp=20)
LargeCargo = ResourceRequirement(interiorplate=360, constcomp=80, computer=8, display=1, 
                                    motor=20, smalltube=60, metalgrid = 24)
O2H2Generator = ResourceRequirement(steelplate = 120, computer = 5, motor = 4, 
                                    largetube = 2, constcomp = 5)
Connector = ResourceRequirement(steelplate = 150, computer = 20, motor = 8, smalltube = 12, constcomp = 40)
Battery = ResourceRequirement(steelplate=80, constcomp = 30, computer=25, powercell=120)
Spotlight = ResourceRequirement(glass=2, constcomp = 20, largetube=2, interiorplate=20, steelplate=8)
Rotor = ResourceRequirement(steelplate=15, motor=4, computer=2, largetube=4, constcomp=10)
LargeRotorHead = ResourceRequirement(largetube=24, steelplate=30)
SolarPanel = ResourceRequirement(constcomp=10, solarcell=64, computer=2, largetube=1, steelplate=4)
Refinery = ResourceRequirement(computer=20, motor=16, largetube=20, constcomp=40, steelplate=1200)
MedBay = ResourceRequirement(interiorplate=240, medcomp=15, computer=10, display=10, largetube=5, 
                           smalltube=20, metalgrid=60, constcomp=80)
ProgramBlock = ResourceRequirement(steelplate=21, computer=2, display=1, motor=1, largetube=2, constcomp=4)
Assembler = ResourceRequirement(steelplate=150, computer=80, display=4, motor=8, constcomp=40)
SmallReactor = ResourceRequirement(steelplate=30+50, computer=25, motor=6, reactorcomp=100, largetube=8, metalgrid=4, constcomp=4)

if __name__ == "__main__":
    definitelynecessary = MedBay+Refinery+Assembler+LargeCargo + O2H2Generator 
    energy = 2*Battery + 10*SolarPanel + 2*LargeRotorHead + 2*Rotor 
    piping = 15*ConveyorJunction + 40*ConveyorTube + 2*Connector 
    structure = 40*LightArmor 
    
    result = definitelynecessary + energy + piping + structure 
    
    print("assembled weight/vol:")
    print(calculate_weight_and_vol(result))
    print("raw mats:")
    print(calculate_raw_mats(result))
    print("raw weight/vol:")
    print(calculate_weight_and_vol(calculate_raw_mats(result)))