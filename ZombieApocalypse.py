"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        num = 0
        while num < len(self._zombie_list):
            yield self._zombie_list[num]
            num += 1

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for item in self._human_list:
            yield item
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        grid_height = self.get_grid_height()
        grid_width = self.get_grid_width()
        visited = poc_grid.Grid(grid_height, grid_width)
        # [[visited.set_empty(row, col) for col in range(self.get_grid_width())] for row in range(self.get_grid_height())]
        distance_field = [[grid_height * grid_width for col in range(grid_width)] for row in range(grid_height)]
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            entity_list = self._zombie_list
        else: 
            entity_list = self._human_list
        for item in entity_list:
            boundary.enqueue(item)
            visited.set_full(item[0], item[1])
            distance_field[item[0]][item[1]] = 0
        
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbor_cell = poc_grid.Grid.four_neighbors(self, current_cell[0], current_cell[1])
            for each_cell in neighbor_cell:
                if visited.is_empty(each_cell[0], each_cell[1]) and self.is_empty(each_cell[0], each_cell[1]):
                    visited.set_full(each_cell[0], each_cell[1])
                    distance_field[each_cell[0]][each_cell[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
                    boundary.enqueue(each_cell)
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        iterate = list(self._human_list)
        self._human_list = []
        for item in iterate:
            distance = dict()
            distance[zombie_distance_field[item[0]][item[1]]] = item
            neighbor_cell = poc_grid.Grid.eight_neighbors(self, item[0], item[1])
            for each_cell in neighbor_cell:
                if self.is_empty(each_cell[0], each_cell[1]):
                    distance[zombie_distance_field[each_cell[0]][each_cell[1]]] = each_cell
            max_distance = max(distance.keys())
            selection = [distance.get(max_distance)]
            moves = random.choice(selection)
            self._human_list.append(moves)
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        iterate = list(self._zombie_list)
        self._zombie_list = []
        for item in iterate:
            distance = dict()
            distance[human_distance_field[item[0]][item[1]]] = item
            neighbor_cell = poc_grid.Grid.four_neighbors(self, item[0], item[1])
            for each_cell in neighbor_cell:
                if self.is_empty(each_cell[0], each_cell[1]):
                    distance[human_distance_field[each_cell[0]][each_cell[1]]] = each_cell
            min_distance = min(distance.keys())
            selection = [distance.get(min_distance)]
            moves = random.choice(selection)
            self._zombie_list.append(moves)
# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#poc_zombie_gui.run_gui(Apocalypse(30, 40))
