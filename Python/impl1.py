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
        """Initialises the mirror and life attributes of cell."""
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
        """Returns the mirror attribute of cell."""
        return self.mirror
    
    def set_mirror(self):
        """Sets the mirror attribute of cell to True."""
        self.mirror = True

    def set_life(self, lifespan):
        """Sets the life attribute of cell to the input parameter."""
        self.life = lifespan


class Beam():
    """A Class to represent a single ray beam.

    Attributes:
        start_coordinates : string 
            Input string that represents the initial entry point
            and direction of a ray. 
        end : boolean
            Whether the ray has reached the end state.
        collision : boolean
            Whether the ray has been absorbed by a mirror.
        curr_row_idx : integer
            Current row index of beam with respect to grid.
        curr_col_idx : integer
            Current column index of bean with respect to grid.
        current_direction : string
            Current direction the beam is moving in.
    """
    def __init__(self, start_coordinates, length, grid):
        self.start_coordinates = start_coordinates
        self.end = False
        self.collision = False
        
        """Initialise curr_row_idx, curr_col_idx and current_direction."""
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

        """Check if a mirror is right beside the beam at initial state.
        If so, set end state to True, reduce mirror life. and print
        output to stdout."""
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
        """Check whether the ray is currently on the same cell as a mirror.
        If yes, to set the ray's end and collision attributes to True, 
        deduct mirror life and print output to stdout."""
        if self.end:
            return None
        
        curr_grid_cell = grid[self.curr_row_idx][self.curr_col_idx]
        if curr_grid_cell.is_mirror():
            self.current_direction = None
            self.end = True
            self.collision = True
            self.print_output()
            curr_grid_cell.deduct_life()
            return None

    def check_mirror(self, grid, length):
        """Check whether mirror(s) exist diagonally adjacent to the ray's
        current location. If yes, to deflect the ray by setting current_direction.
        If deflected, to deduct the life of mirror(s) that deflected the ray."""
        if self.end:
            return None
        
        top_right_mirror = False
        bottom_right_mirror = False
        top_left_mirror = False
        bottom_left_mirror = False

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

    def check_end(self, length):
        """Check whether the ray has passed through FenixBox to the other side.
        If yes, set end attribute to true and print output to stdout."""
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
        """Move the ray one step towards the next cell coordinate by
        incrementing or decrementing the curr_col_idx or curr_row_idx."""
        if self.end:
            return None
        
        if self.current_direction == 'right':
            self.curr_col_idx += 1
        elif self.current_direction == 'left':
            self.curr_col_idx -= 1
        elif self.current_direction == 'up':
            self.curr_row_idx -= 1
        elif self.current_direction == 'down':
            self.curr_row_idx += 1

    def print_output(self):
        """Print formatted output of start and end states to stdout."""
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
    
    def is_end(self):
        """Return whether the ray is in its end state."""
        return self.end


class Session():
    """A Class to represent a simulation session.

    Attributes:
        length : integer 
            The number of holes along a side of FenixBox. 
        mirror_positions : float
            The remaining number of absorption/deflections 
            the mirror can take.
        rays : array
            Initial ray positions and directions to be shot.
        grid : object
            2D array instance of FenixBox for current simulation.
    """
    def __init__(self, length, mirror_positions, rays):
        self.length = length
        self.mirror_positions = mirror_positions
        self.rays = rays
        self.grid = self.createGrid()
    
    def createGrid(self):
        """Creates a 2D array representing the FenixBox grid filled 
        with cells, and sets mirror and life attributes for mirrors."""
        rows = []
        for _ in range(self.length):
            columns = []
            for _ in range(self.length):
                columns.append(Cell())
            rows.append(columns)

        for mirror in self.mirror_positions:
            row_idx = mirror[0] - 1
            col_idx = mirror[1] - 1
            cell = rows[row_idx][col_idx]
            cell.set_mirror()
            if len(mirror) == 3:
                cell.set_life(mirror[2])
        return rows

    def start_simulation(self):
        """Start simulation session by shooting rays one by one into
        self.grid. While the beam is not at its end state, call the
        beam object's methods to check for absorption, deflection, 
        end state and move the ray."""
        for ray in self.rays:
            beam = Beam(ray,self.length,self.grid)
            while not beam.is_end():
                beam.check_collision(self.grid)
                beam.check_mirror(self.grid,self.length)
                beam.check_end(self.length)
                beam.move()