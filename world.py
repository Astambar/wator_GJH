import random
from fish import Fish
from shark import Shark
from pool import Grid

COL = 50
ROW = 50

class World:


    def __init__(self, initial_fish_number, initial_shark_number, row = ROW, columns = COL):
        """
        Initializes the world with a grid and initial populations of fish and sharks.

        Parameters:
            initial_fish_number (int): The initial number of fish.
            initial_shark_number (int): The initial number of sharks.
            ligne (int, optional): The number of rows in the grid. Default is `LIGNE`.
            colonne (int, optional): The number of columns in the grid. Default is `COLONNE`.
        """        
        self.row = row
        self.columns = columns
        self.grid = Grid(row,columns)
        self.list_fishes = []
        self.list_sharks = []
        self.initial_shark_number = initial_shark_number
        self.initial_fish_number = initial_fish_number
    
    def check_death_and_kill(self, shark):
        """
        Checks if the shark's energy is zero or less and removes it from the grid and list.

        If the shark's energy is non-positive, it sets its position in the grid to 0 and removes the shark 
        from the `list_sharks`.

        Parameters:
            shark (Shark): The shark object to check and potentially remove.

        Returns:
            None
        """
        if shark.energy <= 0:
            self.grid.set_value((shark.position),0)
            self.list_sharks.remove(shark)


    def initial_animal_placing(self):
        """
        Places the initial animals (fish and sharks) randomly on the grid.

        The method randomly selects positions on the grid to place the initial number of fish and sharks. 
        It continues until all fish and sharks are placed. Fish are represented by `Fish` objects, and sharks by `Shark` objects.

        Returns:
            None
        """
        while self.initial_shark_number > 0 or self.initial_fish_number > 0: # Continue placing sharks and fish until all have been placed
            choice_random = random.randint(1, 2) # 1 is for fish, 2 for sharks
            generate_col = random.randint(0, self.columns - 1)
            generate_line = random.randint(0, self.row - 1)
            if choice_random == 1 and self.initial_fish_number > 0:
                if self.grid.get_value((generate_line,generate_col)) == 0:
                    self.initial_fish_number -= 1
                    new_fish = Fish((generate_line,generate_col))
                    self.grid.set_value((generate_line,generate_col), new_fish)
                    self.list_fishes.append(new_fish)           
            elif choice_random == 2 and self.initial_shark_number > 0:
                if self.grid.get_value((generate_line,generate_col)) == 0:
                    self.initial_shark_number -= 1
                    new_shark = Shark((generate_line,generate_col))
                    self.grid.set_value((generate_line,generate_col), new_shark)
                    self.list_sharks.append(new_shark)


    def surrounding_scan(self, position:tuple) -> list:
        """
        Scans the surrounding cells of a given position on the grid.

        The method checks the four adjacent cells (up, down, left, right) around the given position and categorizes them 
        into empty cells (`0`), cells containing sharks, or cells containing fish.

        Parameters:
            position (tuple): A tuple (row, column) representing the current position to scan.

        Returns:
            list: A list containing three sub-lists:
                - `water_scan`: List of empty cells (water).
                - `fish_scan`: List of cells containing fish.
                - `shark_scan`: List of cells containing sharks.
        """
        water_scan=[]
        shark_scan=[]
        fish_scan=[]
        directions = [
            ((position[0] - 1) % self.row, position[1]), # Up
            ((position[0] + 1) % self.row,position[1]), # Down
            (position[0],(position[1] - 1) % self.columns), # Left
            (position[0],(position[1] + 1) % self.columns) # Right
        ]
        for coord in directions:
            if self.grid.get_value(coord) == 0:
                water_scan.append(coord)
            elif isinstance(self.grid.get_value(coord), Shark):
                shark_scan.append(coord)
            elif isinstance(self.grid.get_value(coord), Fish):
                fish_scan.append(coord)
        return [water_scan, fish_scan, shark_scan]


    def move_and_reproduction(self, animal):
        """
        Moves an animal and handles its reproduction or eating behavior.

        If the animal is a shark, it may eat a fish if nearby or move to an empty cell. 
        If the shark can reproduce, a new shark is created. Similarly, if the animal is a fish, 
        it may move to an empty cell and reproduce or just move.

        Parameters:
            animal (Fish or Shark): The animal to move and potentially reproduce.

        Returns:
            None
        """
        if animal.chronon == 0: # to avoid that new fishes move
            pass
        else:
            scan_cells = self.surrounding_scan(animal.get_position())
            if isinstance((self.grid.get_value(animal.position)), Shark): #check if animal is a shark
                if scan_cells[1]!= []: # check if around the shark there is at least one fish
                    animal.eat()
                    (x_eaten_fish,y_fish_eaten) = random.choice(scan_cells[1]) # creates a tuple with the position chosen by a random choice where the shark will go
                    (x_temporary,y_temporary) = animal.get_position() #creates a tuple with the current position of the shark
                    self.list_fishes.remove(self.grid.get_value((x_eaten_fish,y_fish_eaten))) # removes the fish that is going to be eaten
                    animal.set_position((x_eaten_fish,y_fish_eaten)) # moves the shark to its new position
                    self.grid.set_value((x_eaten_fish,y_fish_eaten),animal)# updates the values in the grid                                         
                    if animal.reproduction_possibility(): # check if shark can reproduce
                        new_shark = Shark((x_temporary,y_temporary)) # creates a new shark to the previous position of the shark
                        self.list_sharks.append(new_shark) # appends the new shark to the shark list
                        self.grid.set_value((x_temporary,y_temporary), new_shark)
                        animal.reset_reproduction_index()
                    else:
                        self.grid.set_value((x_temporary,y_temporary), 0)
                        animal.reproduction_index_increment()
                elif scan_cells[0]!=[]: # else if there is no fish around but an empty position
                    (x_temporary,y_temporary) = animal.get_position()
                    animal.set_position(random.choice(scan_cells[0]))
                    self.grid.set_value((animal.get_position()), animal)
                    if animal.reproduction_possibility():
                        new_shark = Shark((x_temporary,y_temporary))
                        self.list_sharks.append(new_shark)
                        self.grid.set_value((x_temporary,y_temporary), new_shark)
                        animal.reset_reproduction_index()
                    else:
                        self.grid.set_value((x_temporary,y_temporary), 0)
                        animal.reproduction_index_increment()

            elif isinstance(self.grid.get_value(animal.position), Fish):
                if scan_cells[0]!=[]:
                    (x_temporary,y_temporary) = animal.get_position()
                    animal.set_position(random.choice(scan_cells[0]))
                    self.grid.set_value((animal.get_position()), animal)
                    if animal.reproduction_possibility():
                        animal.reset_reproduction_index()
                        new_fish = Fish((x_temporary,y_temporary))
                        self.list_fishes.append(new_fish)
                        self.grid.set_value((x_temporary,y_temporary), new_fish)
                    else:
                        animal.reproduction_index_increment()
                        self.grid.set_value((x_temporary,y_temporary), 0)

    def move(self, animal):
            if animal.chronon == 0: # to avoid that new fishes move
                pass
    
            else:
                scan_cells = self.surrounding_scan(animal.get_position())

                if isinstance((self.grid.get_value(animal.position)), Shark): #check if animal is a shark
                    if scan_cells[1]!= []: # check if around the shark there is at least one fish
                        animal.eat()
                        (x_eaten_fish,y_fish_eaten) = random.choice(scan_cells[1]) # creates a tuple with the position chosen by a random choice where the shark will go
                        (x_temporary,y_temporary) = animal.get_position()
                        self.list_fishes.remove(self.grid.get_value((x_eaten_fish,y_fish_eaten)))
                        animal.set_position((x_eaten_fish,y_fish_eaten))
                        self.grid.set_value((x_eaten_fish,y_fish_eaten), animal)
                        self.grid.set_value((x_temporary,y_temporary), 0)

                    elif scan_cells[0]!=[]:
                        (x_temporary,y_temporary) = animal.get_position()
                        animal.set_position(random.choice(scan_cells[0]))
                        self.grid.set_value((animal.get_position()), animal)
                        self.grid.set_value((x_temporary,y_temporary), 0)

                elif isinstance(self.grid.get_value(animal.position), Fish):
                    if scan_cells[0]!=[]:
                        (x_temporary,y_temporary) = animal.get_position()
                        animal.set_position(random.choice(scan_cells[0]))
                        animal.reproduction_index_increment()
                        self.grid.set_value((animal.get_position()), animal)
                        self.grid.set_value((x_temporary,y_temporary), 0)
        

    def reproduction(self, animal):
        scan_cells = self.surrounding_scan(animal.get_position())

        if isinstance((self.grid.get_value(animal.position)), Shark): #check if animal is a shark
            if scan_cells[0] != [] and scan_cells[1] != 0:
                (x_temporary,y_temporary) = animal.get_position() # moves the shark to its new position
                new_shark = Shark((x_temporary,y_temporary)) # creates a new shark to the previous position of the shark
                self.list_sharks.append(new_shark) # appends the new shark to the shark list
                animal.reset_reproduction_index()

        elif isinstance((self.grid.get_value(animal.position)), Fish): #check if animal is a shark
            if scan_cells[0] != []:
                (x_temporary,y_temporary) = animal.get_position() # moves the shark to its new position
                new_fish = Fish((x_temporary,y_temporary)) # creates a new shark to the previous position of the shark
                self.list_fishes.append(new_fish) # appends the new shark to the shark list
                animal.reset_reproduction_index()

    def reproduction_move_2(self, animal):

        if animal.reproduction_index == animal.childbirth_value:
            self.reproduction(animal)
            self.move(animal)
        
        else:
            self.move(animal)
            animal.reproduction_index_increment()