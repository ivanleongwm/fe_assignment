class Cell():
    """A Class to represent a single cell in the FenixBox grid.

    Attributes:
        mirror : boolean 
            Whether the cell is a mirror or not. 
        life : float
            The remaining number of absorption/deflections 
            the mirror can take.
    """
    def __init__(self):
        self.mirror = False
        self.life = float('inf')

    def deduct_life(self):
        """Reduces the life of mirror cell upon absorption/deflection.
        If life is zero, cell ceases to be a mirror.
        """
        self.life -= 1
        if self.life == 0:
            self.mirror = False
            self.life = float('inf')
    
    def is_mirror(self):
        return self.mirror
    
    def set_mirror(self):
        self.mirror = True

    def set_life(self, lifespan):
        self.life = lifespan


class Beam():
    # Beam Class
    def __init__(self, start_coordinates, length, grid):
        self.start_coordinates = start_coordinates
        self.end = False
        self.collision = False
        # Initialise the starting coordinates of the beam
        if start_coordinates[0] == 'R' and start_coordinates[2] == '+':
            self.curr_row_idx = int(start_coordinates[1]) - 1
            self.curr_col_idx = 0
            self.current_direction = 'right'
        elif start_coordinates[0] == 'R' and start_coordinates[2] == '-':
            self.curr_row_idx = int(start_coordinates[1]) - 1
            self.curr_col_idx = length - 1
            self.current_direction = 'left'
        elif start_coordinates[0] == 'C' and start_coordinates[2] == '+':
            self.curr_row_idx = 0
            self.curr_col_idx = int(start_coordinates[1]) - 1
            self.current_direction = 'down'
        elif start_coordinates[0] == 'C' and start_coordinates[2] == '-':
            self.curr_row_idx = length - 1
            self.curr_col_idx = int(start_coordinates[1]) - 1
            self.current_direction = 'up'
        #print('Original Beam Position:',self.current_direction,self.curr_row_idx+1,self.curr_col_idx+1)

        # If mirror right beside end immediately
        if start_coordinates[0] == 'C':
            if not (self.curr_col_idx == 0):
                left_cell = grid[self.curr_row_idx][self.curr_col_idx - 1]
                if left_cell.is_mirror():
                    self.end = True
                    self.print_output()
                    left_cell.deduct_life()
            if not (self.curr_col_idx == (length - 1)):
                right_cell = grid[self.curr_row_idx][self.curr_col_idx + 1]
                if right_cell.is_mirror():
                    self.end = True
                    self.print_output()
                    right_cell.deduct_life()
        if start_coordinates[0] == 'R':
            if not (self.curr_row_idx == 0):
                top_cell = grid[self.curr_row_idx - 1][self.curr_col_idx]
                if top_cell.is_mirror():
                    self.end = True
                    self.print_output()
                    top_cell.deduct_life()
            if not (self.curr_row_idx == (length - 1)):
                bottom_cell = grid[self.curr_row_idx + 1][self.curr_col_idx]
                if bottom_cell.is_mirror():
                    self.end = True
                    self.print_output()
                    bottom_cell.deduct_life()
    
    def check_collision(self, grid):
        if self.end:
            return None
        # Check if current cell is a mirror
        #print("test",self.current_direction,self.curr_row_idx,self.curr_col_idx)
        curr_grid_cell = grid[self.curr_row_idx][self.curr_col_idx]
        if curr_grid_cell.is_mirror():
            self.current_direction = None
            self.end = True
            self.collision = True
            self.print_output()
            curr_grid_cell.deduct_life()
            return None

    def check_mirror(self, grid, length):
        if self.end:
            return None
        
        top_right_mirror = False
        bottom_right_mirror = False
        top_left_mirror = False
        bottom_left_mirror = False

        # Check whether adjacent diagonals are mirrors and redirect
        if not (self.curr_col_idx == length - 1) and not (self.curr_row_idx == 0):
            top_right_cell = grid[self.curr_row_idx - 1][self.curr_col_idx + 1]
            top_right_mirror = top_right_cell.is_mirror()
        if not (self.curr_col_idx == length - 1) and not (self.curr_row_idx == length - 1):
            bottom_right_cell = grid[self.curr_row_idx + 1][self.curr_col_idx + 1]
            bottom_right_mirror = bottom_right_cell.is_mirror()
        if not (self.curr_col_idx == 0) and not (self.curr_row_idx == 0):
            top_left_cell = grid[self.curr_row_idx - 1][self.curr_col_idx - 1]
            top_left_mirror = top_left_cell.is_mirror()
        if not (self.curr_col_idx == 0) and not (self.curr_row_idx == length - 1):
            bottom_left_cell = grid[self.curr_row_idx + 1][self.curr_col_idx - 1]
            bottom_left_mirror = bottom_left_cell.is_mirror()

        if self.current_direction == 'right':
            if top_right_mirror and bottom_right_mirror:
                self.current_direction = 'left'
                top_right_cell.deduct_life()
                bottom_right_cell.deduct_life()
            elif  top_right_mirror:
                self.current_direction = 'down'
                top_right_cell.deduct_life()
            elif bottom_right_mirror:
                self.current_direction = 'up'
                bottom_right_cell.deduct_life()

        elif self.current_direction == 'left':
            if top_left_mirror and bottom_left_mirror:
                self.current_direction = 'right'
                top_left_cell.deduct_life()
                bottom_left_cell.deduct_life()
            elif top_left_mirror:
                self.current_direction = 'down'
                top_left_cell.deduct_life()
            elif  bottom_left_mirror:
                self.current_direction = 'up'
                bottom_left_cell.deduct_life()

        elif self.current_direction == 'up':
            if top_left_mirror and top_right_mirror:
                self.current_direction = 'down'
                top_left_cell.deduct_life()
                top_right_cell.deduct_life()
            elif top_left_mirror:
                self.current_direction = 'right'
                top_left_cell.deduct_life()
            elif top_right_mirror:
                self.current_direction = 'left'
                top_right_cell.deduct_life()

        elif self.current_direction == 'down':
            if bottom_left_mirror and bottom_right_mirror:
                self.current_direction = 'up'
                bottom_left_cell.deduct_life()
                bottom_right_cell.deduct_life()
            elif bottom_left_mirror:
                self.current_direction = 'right'
                bottom_left_cell.deduct_life()
            elif bottom_right_mirror:
                self.current_direction = 'left'
                bottom_right_cell.deduct_life()
        #print("Check bot left mirror",bottom_left_mirror)

    def check_end(self, length):
        if self.current_direction == 'up' and self.curr_row_idx == 0:
            self.end = True
            self.print_output()
        elif self.current_direction == 'right' and self.curr_col_idx == (length - 1):
            self.end = True
            self.print_output()
        elif self.current_direction == 'down' and self.curr_row_idx == (length - 1):
            self.end = True
            self.print_output()
        elif self.current_direction == 'left' and self.curr_col_idx == 0:
            self.end = True
            self.print_output()
    
    def move(self):
        if self.end:
            return None
        # Move beam one step in current direction
        if self.current_direction == 'right':
            self.curr_col_idx += 1
        elif self.current_direction == 'left':
            self.curr_col_idx -= 1
        elif self.current_direction == 'up':
            self.curr_row_idx -= 1
        elif self.current_direction == 'down':
            self.curr_row_idx += 1

    def print_output(self):
        if self.collision:
            print(f"{self.start_coordinates} ->")
        else:
            print(self.start_coordinates
                  + ' -> '
                  + '{'
                  + str(self.curr_row_idx + 1)
                  + ','
                  + str(self.curr_col_idx + 1)
                  + '}')


class Session():
    def __init__(self, length, mirror_positions, rays):
        self.length = length
        self.mirror_positions = mirror_positions
        self.rays = rays
        self.grid = self.createGrid()
    
    def createGrid(self):
        # Create Empty Grid
        rows = []
        for _ in range(self.length):
            columns = []
            for _ in range(self.length):
                columns.append(Cell())
            rows.append(columns)
        #print(rows)

        # Insert Mirrors
        for mirror in self.mirror_positions:
            row_idx = mirror[0] - 1
            col_idx = mirror[1] - 1
            cell = rows[row_idx][col_idx]
            cell.set_mirror()
            if len(mirror) == 3:
                cell.set_life(mirror[2])
        return rows

    def start_simulation(self):
        for ray in self.rays:
            beam = Beam(ray,self.length,self.grid)
            while not beam.end:
                #print(beam.curr_row_idx+1,beam.curr_col_idx+1)
                beam.check_collision(self.grid)
                beam.check_mirror(self.grid,self.length)
                beam.check_end(self.length)
                beam.move()
                #print(beam.curr_row_idx+1,beam.curr_col_idx+1)