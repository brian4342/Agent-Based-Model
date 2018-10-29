import random
import matplotlib.pyplot as plt
import matplotlib.animation 
import agents as AgentFR
import matplotlib.widgets
import TerrainGenerator


class ABM:
    # Initialise Agent Based Model
    def __init__(self, num_of_sheep, num_of_Wolf, num_of_iterations, map_size, seed):
        self.environment = []
        self.agents = []
        self.num_of_sheep = num_of_sheep
        self.num_of_Wolf = num_of_Wolf
        self.num_of_iterations = num_of_iterations
        self.neighbourhood = 20
        self.fig = plt.figure(figsize=(7, 7))
        self.map_size = map_size
        self.seed = seed
    
    # Generate random terrain
    def Set_Environment(self):
        self.environment = TerrainGenerator.MakeTerrain(self.map_size, self.seed)
    
    # Update method for simulation
    def update(self, frame_number):
        #self.Remove_Dead() 
        random.shuffle(self.agents) # Shuffle the agents to randomise their order
        self.fig.clear() # Clear the figure
        
        #plt.ion()
        plt.ylim(0, len(self.environment)) # Set the boundaries
        plt.xlim(0, len(self.environment))
        
        plt.xticks([]) # Remove the axis from the graph
        plt.yticks([])
        
        # Make the agents perform an action
        for index in range(0,len(self.agents)):
            self.agents[index].Decide_Action()
        
        # Annotate the graph with the data
        plt.title('Timestep:' + str(frame_number))
        sheeps = [x for x in self.agents if x.type == 'Sheep']
        wolves = [x for x in self.agents if x.type == 'Wolf']
        plt.xlabel('Sheep Population: ' + str(len(sheeps)) + '\n' + 'Wolf Population: ' + str(len(wolves)) + '\n' + 'Terrain Size: ' 
                   + str(len(self.environment)) + 'x' + str(len(self.environment)))
        
        # Add the environment to the graph
        plt.imshow(self.environment, vmin=0, vmax=250, cmap='summer_r')
        plt.colorbar()
        
        # Add the agents to the graph
        for index in range(0,len(self.agents)):
            plt.scatter(self.agents[index].x, self.agents[index].y, c=self.agents[index].color, edgecolors='black')
            annotate_text = self.agents[index].type + "\n" + str(self.agents[index].store)
            plt.annotate(annotate_text, (self.agents[index].x, self.agents[index].y), annotation_clip=False)
            
        # Save the figure as PNG to later turn into a GIF    
        #plt.savefig('C:/Users/495786/Dropbox/Sheffield PhD/Final ABM/Results/iteration ' + str(frame_number) + '.png')
        self.Remove_Dead() # remove all dead agents from array
        
        #Re-grow Grass
        #self.Grow_Grass()
        #self.environment = [x+0.01 for x in self.environment ]
        
    def Grow_Grass(self):
        # randomly grow 5% of environments grass count 
        """
        for index in range(0,int(len(self.environment)*0.05)):
            randomX = random.randint(0, len(self.environment)-1)
            randomY = random.randint(0, len(self.environment)-1)
            if self.environment[randomX][randomY] < 200:
                self.environment[randomX][randomY] += 5
        """
        # Need more efficent grass growing function. 
        """
        for index in range(0,len(self.environment)):
            for index2 in range(0,len(self.environment[index])):
                if self.environment[index][index2] < 250:
                    self.environment[index][index2] += 1
        """
        
    def Reset(self):
        # Reset the environemnt and agent list
        self.environment = []
        self.agents = []
        
    def Set_Agents(self):
        # Generate the agents based on the given parameters
        for index in range(0,self.num_of_sheep):
            self.agents.append(AgentFR.Sheep(self.environment, self.agents))
        
        for index in range(0,int(self.num_of_Wolf)):
            self.agents.append(AgentFR.Wolf(self.environment, self.agents))
    
    def Remove_Dead(self):
        # Remove all dead agents
        self.agents[:] = [x for x in self.agents if x.type != 'Dead']
        
    def Start(self):
        #Initialise Environment and Agent
        self.Reset()
        self.Set_Environment()
        self.Set_Agents()

        plt.rc('font', size=8) 
        plt.rc('axes', titlesize=22)
        animation = matplotlib.animation.FuncAnimation(self.fig, self.update, frames=self.num_of_iterations, repeat=False)
        plt.show(block=True)
        print('working ABM Class')
        return animation