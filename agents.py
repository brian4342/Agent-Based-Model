import random

class Agent:
    
    def __init__(self, environment, agents):
        self.x = random.randint(0,len(environment)-1)
        self.y = random.randint(0,len(environment[0])-1)
        self.environment = environment
        self.agents = agents
        self.store = 40
        self.alive = True
    
    def Move(self): # Random Move Method
        # Get next Y-Postion
        random_number = random.random()
        if random_number > 0.5:
            self.y = (self.y + 1) % len(self.environment[0]) # Modulus to allow agent to tarus the map
        else:
            self.y = (self.y - 1) % len(self.environment[0])
        
        # Get next X-Position
        random_number = random.random()
        if random_number > 0.5:
            self.x = (self.x + 1) % len(self.environment)
        else:
            self.x = (self.x - 1) % len(self.environment)
        
        #Cost to Move
        self.store -= 10
        
    def Decide_Action(self):
        # Basic agent can only move 
        # Advanced agents can override this method
        self.Move()
        self.Check_Death()
        
    def Check_Death(self):
        # Check for death    
        if self.store < 5:
            self.alive = False
            self.type = 'Dead'

class Sheep(Agent):
    
    def __init__(self, environment, agents):
        # Sheep inherits from Agent class
        Agent.__init__(self,environment, agents)
        self.type = "Sheep"
        self.color = "White"
        
    def Eat(self):
        # Sheep eat method 
        # Sheep eat and modify the terrain
        if self.environment[self.y][self.x] > 30:
            self.environment[self.y][self.x] -= 30
            self.store += 30 
        elif self.environment[self.y][self.x] > 0: # Eat remainder of terrain
            self.store += self.environment[self.y][self.x]
            self.environment[self.y][self.x] = 0
        else: 
            # IF there is no food in current location
            # Go Find Food
            self.Move() 
    
    def Decide_Action(self):
        # Override the Decide_Action method 
        # Logic:
            # 1. Check if agent is 'Safe'
            # 2. If agent is not 'Safe' then Run away 
            # 3. If agent is 'Safe' then Eat / Move
        try:    
            wolf = self.Safe() #Check for Wolves
        
            if wolf == None: # No Wolves Nearby
                if self.store >= 200: # If sheep is not Hungry
                    if random.randrange(0,100) >= 85: # 85% to Move || 15% to Eat more
                        self.Eat()
                    else:
                        self.Mate()
                elif self.store < 200: # Sheep is Hungry
                    self.Eat() # Sheep will eat at currently location, if location is empty then it will move
            else: # Wolf Nearby
                
                # Find Direction and Distance of Wolf
                steps_number = max( abs(wolf.x - self.x), abs(wolf.y - self.y))
                if steps_number == 0:
                    steps_number = 1
                
                stepx = float(wolf.x - self.x)/steps_number
                stepy = float(wolf.y - self.y)/steps_number
                
                # Calculate if the sheep has enough energy to run
                run_steps = 3
                if self.store > 100: #Has Energy to Run
                    run_steps = 3
                else: #Out of energy
                    run_steps = 2
                
                # Move away from Wolf
                for i in range(1,min(run_steps,steps_number)):
                    self.x = int(self.x - stepx*i) % len(self.environment[0])
                    self.y = int(self.y - stepy*i) % len(self.environment[0])
                    self.store -= 10
            self.Check_Death()
        except Exception as e:
            # Catch exception
            self.Move()
            print('Decide Action Error: ' + str(e) )
            
    def Move_to_Mate(self, closest_sheep):
         try:
            # Move Towards closest Sheep
            steps_number = max( abs(closest_sheep.x - self.x), abs(closest_sheep.y - self.y))
            stepx = float(closest_sheep.x - self.x)/steps_number
            stepy = float(closest_sheep.y - self.y)/steps_number
            
            self.x = int(self.x + stepx) % len(self.environment[0])
            self.y = int(self.y + stepy) % len(self.environment[0])
            self.store -= 10
            self.Check_Death()
         except Exception as e:
            # Catch exception
            self.Move()
            print('Move to Mate Error: ' + str(e) )
            
    def Mate(self):
         try:
            shortest_distance = len(self.environment) # Initialise the shortest distance to maximum 
            closest_sheep = None
            
            #Find Closest Sheep
            sheeps = [x for x in self.agents if x.type == 'Sheep'] # Get list of all Sheep Agents
            for index in range(0,len(sheeps)):
                if self != sheeps[index]:
                    
                    distance = Calc_Distance(self.x, self.y, sheeps[index].x, sheeps[index].y)
                    if distance < shortest_distance:
                        shortest_distance = distance
                        closest_sheep = sheeps[index] # Select the closest sheep to Mate
            
            if closest_sheep != None:
                if shortest_distance < 2 and self.store >= 200:
                    # Make a new Sheep
                    self.agents.append(Sheep(self.environment, self.agents))
                    self.agents[len(self.agents)-1].x = self.x
                    self.agents[len(self.agents)-1].y = closest_sheep.y
                    self.store = round((self.store * 0.1),1)
                    closest_sheep.store = round((self.store * 0.1),1)
                else:
                    # Move to the Sheep
                    self.Move_to_Mate(closest_sheep)
            else: # No Sheep
                self.Move()
         except Exception as e:
            # Catch exception
            self.Move()
            print('Mate Error: ' + str(e) ) 
    
    def Safe(self):
        # This method will search through all Wolf Agents 
        # A sheep is in danger if there is a Wolf close by
        
        try:
            shortest_distance = len(self.environment) # Initialise the shortest distance to maximum 
            closest_wolf = None
            
            #Find Closest Wolf
            wolves = [x for x in self.agents if x.type == 'Wolf'] # Get list of all Wolf Agents
            for index in range(0,len(wolves)):
                distance = Calc_Distance(self.x, self.y, wolves[index].x, wolves[index].y)
                if distance < shortest_distance:
                        shortest_distance = distance
                        closest_wolf = wolves[index]
                                    
            #If wolf then run else eat/move
            if closest_wolf != None:
                if shortest_distance < 15: # If wolf is close return the wolf's index
                    return closest_wolf
                else:
                    return None  # Sheep is safe
            else:
                return None # Sheep is safe
        except Exception as e:
            # Catch exception
            print('Safety Check Error: ' + str(e) )
            
            
class Wolf(Agent):
    
    def __init__(self, environment, agents):
        Agent.__init__(self, environment, agents)
        self.type = "Wolf"
        self.color = "Red"
        self.rest_count = 0 
        self.store = 100
    
    def Decide_Action(self):
        if self.rest_count > 0: # Wolf should rest after eating sheep
            self.rest_count -= 1
        else:
            self.Kill() # Wolf can begin the Hunt for sheep
            self.Check_Death()
    
    def Kill(self):
        # This method will identify the closest sheep to the Wolf 
        # The Wolf will either move to the sheep or kill the sheep if close enough 
        try:
            shortest_distance = len(self.environment) # Initialise the shortest distance to maximum 
            closest_sheep = None
            
            #Find Closest Sheep
            sheeps = [x for x in self.agents if x.type == 'Sheep'] # Get list of all Sheep Agents
            #print("Sheep count: " + str(len(sheeps)))
            #print("Shortest Distance before: " + str(shortest_distance))
            
            for index in range(0,len(sheeps)):
                distance = Calc_Distance(self.x, self.y, sheeps[index].x, sheeps[index].y)
                if distance < shortest_distance:
                    shortest_distance = distance
                    closest_sheep = sheeps[index] # Select the closest sheep to hunt
            #print("Shortest Distance after: " + str(shortest_distance))
            
            if closest_sheep != None:
                if shortest_distance < 2:
                    # Eat the Sheep
                    closest_sheep.alive = False
                    closest_sheep.type = 'Dead'
                    self.store += closest_sheep.store
                    
                    # Force wolf to rest after kill
                    #self.rest_count = 20
                else:
                    # Hunt the Sheep
                    self.Hunt(closest_sheep)
            else: # No Sheep (Wolf will starve)
                print('no Sheep')
                self.Move()
            
        except Exception as e:
            # Catch exception
            self.Move()
            print('Kill Check Error: ' + str(e) ) 
      
    def Hunt(self, closest_sheep):
        try:
            # Move Towards Sheep
            steps_number = max( abs(closest_sheep.x - self.x), abs(closest_sheep.y - self.y))
            stepx = float(closest_sheep.x - self.x)/steps_number
            stepy = float(closest_sheep.y - self.y)/steps_number
            
            min_steps = 3 # Wolf can run if sheep close
            if steps_number > 20: # Sheep too far away, so walk
                min_steps = 2
            
            for i in range(1,min(min_steps,steps_number)): 
                self.x = int(self.x + stepx*i) % len(self.environment[0])
                self.y = int(self.y + stepy*i) % len(self.environment[0])
                # Movement cost based on size of map. Wolf should be able to walk half the map
                cost = 100/(len(self.environment)/2)
                self.store -= cost # wolves are energy efficient 
            self.store = round(self.store,1)
            self.Check_Death()
        except Exception as e:
            # Catch exception
            self.Move()
            print('Hunt Check Error: ' + str(e) )
            
def Calc_Distance(x0, y0, x1, y1):
    # Calculate and return the distance between agents.
    distance = (((y0 - y1)**2) + ((x0 - x1)**2))**0.5
    return distance