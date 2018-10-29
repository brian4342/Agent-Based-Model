import tkinter
import ABM
from random import randint

entries = []
animation = None

# Use this method to send the parameters to the ABM
def fetch(entries):
    print('ABM Started...')
    global animation
    
    num_of_iterations = int(entries[0][1].get())
    num_of_sheep = int(entries[1][1].get())
    num_of_wolf = int(entries[2][1].get())
    seed = int(entries[3][1].get())
    map_size = int(entries[4][1].get())
    
    # Create ABM instance
    abm_instance = ABM.ABM(num_of_sheep, num_of_wolf, num_of_iterations, map_size, seed)
    animation = abm_instance.Start()
    
# Generate the Form
def makeform(root): 
    row = tkinter.Frame(root)
    create_form_field(row, 'Simulation Duration', 10000)
    create_form_field(row, 'Sheep Count', 100)
    create_form_field(row, 'Wolf Count', 100)
    create_form_field(row, 'Seed', 10000)
    create_form_field(row, 'Map Size', 1000)
    return entries    

def create_form_field(row, field, max_range):
    # Auto Generate the form
    row = tkinter.Frame(root)
    lab = tkinter.Label(row, width=15, text=field, anchor='w')
    scale = tkinter.Scale(row, orient='horizontal', from_=0, to=max_range)
    row.pack(side=tkinter.TOP, fill=tkinter.X, padx=5, pady=5)
    lab.pack(side=tkinter.LEFT)
    scale.pack(side=tkinter.RIGHT, expand=tkinter.YES)
    entries.append((field, scale))

# Create ABM based on random values
def randomABM():
    global animation
    
    # Get random parameters for ABM
    num_of_sheep = randint(0,100)
    num_of_wolf = randint(0,100)
    num_of_iterations = randint(0,1000)
    map_size = randint(200,1000)
    seed = randint(0,10000)
    
    abm_instance = ABM.ABM(num_of_sheep, num_of_wolf, num_of_iterations, map_size, seed)
    animation = abm_instance.Start()
    print('Random ABM Started...')

# Run the program
if __name__ == '__main__':
   root = tkinter.Tk()
   ents = makeform(root)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
   b1 = tkinter.Button(root, text='Start ABM', command=(lambda e=ents: fetch(e)))
   b1.pack(side=tkinter.LEFT, padx=5, pady=5)
   b2 = tkinter.Button(root, text='Random ABM', command=(randomABM))
   b2.pack(side=tkinter.LEFT, padx=5, pady=5)
   b3 = tkinter.Button(root, text='Quit', command=root.quit)
   b3.pack(side=tkinter.LEFT, padx=5, pady=5)
   root.mainloop()