
class Cell():
    # Cell Class
    def __init__(self) -> None:
        self.mirror = False
        self.life = float('inf')

def createGrid(length,mirror_positions):
    # Create Empty Grid
    rows = []
    for _ in range(length):
        columns = []
        for _ in range(length):
            columns.append(Cell())
        rows.append(columns)
    #print(rows)

    # Insert Mirrors
    for mirror in mirror_positions:
        row_idx = mirror[0] - 1
        col_idx = mirror[1] - 1
        cell = rows[row_idx][col_idx]
        cell.mirror = True
        if len(mirror) == 3:
            cell.life = mirror[2] 
    return rows


class Beam():
    # Beam Class
    def __init__(self,start_coordinates,length,grid) -> None:
        self.start_coordinates = start_coordinates
        self.end = False
        # Initialise the starting coordinates of the beam
        if start_coordinates[0]=='R' and start_coordinates[2]=='+':
            self.curr_row_idx = int(start_coordinates[1]) - 1 
            self.curr_col_idx = 0
            self.current_direction = 'right'
        elif start_coordinates[0]=='R' and start_coordinates[2]=='-':
            self.curr_row_idx = int(start_coordinates[1]) - 1
            self.curr_col_idx = length - 1
            self.current_direction = 'left'    
        elif start_coordinates[0]=='C' and start_coordinates[2]=='+':
            self.curr_row_idx = 0
            self.curr_col_idx = int(start_coordinates[1]) - 1
            self.current_direction = 'down'
        elif start_coordinates[0]=='C' and start_coordinates[2]=='-':
            self.curr_row_idx = length - 1
            self.curr_col_idx = int(start_coordinates[1]) - 1
            self.current_direction = 'up'

        #print('Original Beam Position:',self.current_direction,self.curr_row_idx+1,self.curr_col_idx+1)

        # If mirror right beside end immediately
        if start_coordinates[0]=='C':
            if not (self.curr_col_idx == 0):
                if grid[self.curr_row_idx][self.curr_col_idx - 1].mirror:
                    self.end = True
                    self.print_output()
            if not (self.curr_col_idx == (length - 1)):
                if grid[self.curr_row_idx][self.curr_col_idx + 1].mirror:
                    self.end = True
                    self.print_output()
        if start_coordinates[0]=='R':
            if not (self.curr_row_idx == 0):
                if grid[self.curr_row_idx - 1][self.curr_col_idx].mirror:
                    self.end = True
                    self.print_output()
            if not (self.curr_row_idx == (length - 1)):
                if grid[self.curr_row_idx + 1][self.curr_col_idx].mirror:
                    self.end = True
                    self.print_output()
    
    def check_collision(self,grid):
        if self.end:
            return None
        # Check if current cell is a mirror
        #print("test",self.current_direction,self.curr_row_idx,self.curr_col_idx)
        curr_grid_cell = grid[self.curr_row_idx][self.curr_col_idx]
        if curr_grid_cell.mirror == True:
            self.current_direction = None
            self.end = True
            print(self.start_coordinates,'->')
            curr_grid_cell.life -= 1
            if curr_grid_cell.life == 0:
                curr_grid_cell.mirror = False
                curr_grid_cell.life = float('inf')
            return None

    def check_mirror(self,grid,length):
        if self.end:
            return None
        top_right_mirror = False
        bottom_right_mirror = False
        top_left_mirror = False
        bottom_left_mirror = False

        # Check whether adjacent diagonals are mirrors and redirect
        if not (self.curr_col_idx == length - 1) and not (self.curr_row_idx == 0):
            top_right_mirror = grid[self.curr_row_idx-1][self.curr_col_idx+1].mirror
        if not (self.curr_col_idx == length - 1) and not (self.curr_row_idx == length - 1):
            bottom_right_mirror = grid[self.curr_row_idx+1][self.curr_col_idx+1].mirror
        if not (self.curr_col_idx == 0) and not (self.curr_row_idx == 0):
            top_left_mirror = grid[self.curr_row_idx-1][self.curr_col_idx-1].mirror
        if not (self.curr_col_idx == 0) and not (self.curr_row_idx == length - 1):
            bottom_left_mirror = grid[self.curr_row_idx+1][self.curr_col_idx-1].mirror

        if self.current_direction  == 'right':
            if top_right_mirror and bottom_right_mirror:
                self.current_direction = 'left'
            elif  top_right_mirror:
                self.current_direction = 'down'
            elif bottom_right_mirror:
                self.current_direction = 'up'

        elif self.current_direction  == 'left':
            if top_left_mirror and bottom_left_mirror:
                self.current_direction = 'right'
            elif top_left_mirror:
                self.current_direction = 'down'
            elif  bottom_left_mirror:
                self.current_direction = 'up'

        elif self.current_direction  == 'up':
            if top_left_mirror and top_right_mirror:
                self.current_direction = 'down'
            elif top_left_mirror:
                self.current_direction = 'right'
            elif top_right_mirror:
                self.current_direction = 'left'

        elif self.current_direction  == 'down':
            if bottom_left_mirror and bottom_right_mirror:
                self.current_direction = 'up'
            elif bottom_left_mirror:
                self.current_direction = 'right'
            elif bottom_right_mirror:
                self.current_direction = 'left'

        #print("Check bot left mirror",bottom_left_mirror)

    def print_output(self):
        print(self.start_coordinates,'->','{'+str(self.curr_row_idx + 1)+','+str(self.curr_col_idx + 1)+'}')

    def check_end(self,length):
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
        if self.current_direction  == 'right':
            self.curr_col_idx += 1
        elif self.current_direction  == 'left':
            self.curr_col_idx -= 1
        elif self.current_direction  == 'up':
            self.curr_row_idx -= 1
        elif self.current_direction  == 'down':
            self.curr_row_idx += 1


class Session():
    def __init__(self,length,mirror_positions,rays):
        self.length = length
        self.mirror_positions = mirror_positions
        self.rays = rays
        self.grid = createGrid(length,mirror_positions)
    
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
