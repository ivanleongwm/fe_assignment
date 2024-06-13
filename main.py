if __name__ == '__main__':
    import sys
    import re
    import argparse
    from logic import Session


class File():
    """A Class to represent a file.
    
    Attributes:
        filename : string
            Name of the file in the main script directory.
        debug_mode : boolean
            Whether to print validation error messages to stdout.
    """
    def __init__(self,filename, debug_mode):
        self.filename = filename
        self.debug_mode = debug_mode

    def get_file_lines(self):
        """Read file contents into an array separated by newlines."""
        try:
            with open(self.filename) as file:
                lines = file.read().splitlines()
                return lines
        except IOError:
            if self.debug_mode:
                print(f'Could not read file: {self.filename}. Please check file name or directory.')
            sys.exit(3)


class DesignFile(File):
    """A Class to represent a design file. 
    Inherits attribute and method from parent File class.
    
    Attributes:
        file_lines : array
            Each line of file stored in an array.
        mirror_regex : string
            Regular expression string to match mirror coordinates and life.
        holes : int
            Number of holes on one side of FenixBox.
        mirrors : array
            Array of mirror coordinates and life.
        error : boolean
            Whether the design file contains an error or not.
    """
    def __init__(self, filename, debug_mode):
        super().__init__(filename, debug_mode)
        self.file_lines = self.get_file_lines()
        self.mirror_regex = r'^[1-9][0-9]*\s[1-9][0-9]*\s?([1-9][0-9]*)*$'
        self.holes = None
        self.mirrors = self.parse_mirrors()
        self.error = False
    
    def validate(self):
        """Calls methods to check for errors in holes and mirrors."""
        self.check_holes_error()
        self.check_mirror_error()

    def check_holes_error(self):
        """Checks for missing number of holes or wrong order of holes number."""
        for line in self.file_lines:
            if re.match(self.mirror_regex, line):
                if self.debug_mode:
                    print('Number of holes in FenixBox should be on first uncommented line.')
                self.error = True
                return None
            elif line.isdigit():
                self.holes = int(line)
                return None
        if self.debug_mode:    
            print('Number of holes in FenixBox missing from design file.')
        self.error = True

    def check_mirror_error(self):
        """Checks for invalid mirror coordinate/ life syntax and prints error line."""
        if self.holes:
            mirror_index = self.file_lines.index(str(self.holes)) + 1
        else:
            mirror_index = 0
        mirror_lines = self.file_lines[mirror_index:]
        for idx, line in enumerate(mirror_lines):
            if (not re.match(self.mirror_regex,line)) and (line != '') and (not line.startswith('#')):
                self.error = True
                if self.debug_mode:
                    print(f'Invalid Mirror: "{line}" on Line {idx + mirror_index + 1} of design file.')

    def parse_mirrors(self):
        """Convert mirror string coordinates/ life into one list of integers per mirror."""
        mirrors = []
        for line in self.file_lines:    
            if re.match(self.mirror_regex, line):
                mirrors.append([int(mirror) for mirror in line.split()])
        return mirrors

    def has_error(self):
        """Returns whether there is an error in the design file."""
        return self.error

    def get_holes(self):
        """Returns the number of holes on one side of FenixBox."""
        return self.holes
    
    def get_mirrors(self):
        """Returns the array of mirrors in FenixBox."""
        return self.mirrors
    
class TestFile(File):
    """A Class to represent a test file. 
    Inherits attribute and method from parent File class.
    
    Attributes:
        file_lines : array
            Each line of file stored in an array.
        ray_regex : string
            Regular expression string to match ray coordinates and direction.
        rays : array
            List of ray strings extracted from the test file.
        error : boolean
            Whether the test file contains an error or not.
    """
    def __init__(self, filename, debug_mode):
        super().__init__(filename, debug_mode)
        self.file_lines = self.get_file_lines()
        self.ray_regex = r'^[CR][1-9][0-9]*[+-]$'
        self.rays = self.parse_rays()
        self.error = False

    def validate(self):
        """Calls methods to check for errors in rays."""
        self.check_rays_error()

    def check_rays_error(self):
        """Checks for invalid ray syntax and prints error line."""
        for idx, line in enumerate(self.file_lines):
            if (not re.match(self.ray_regex, line)) and (line != '') and (not line.startswith('#')):
                self.error = True
                if self.debug_mode:
                    print(f'Invalid Ray: "{line}" on Line {idx + 1} of testfile.')

    def parse_rays(self):
        """Extract valid ray coordinates/ direction into list."""
        return [l for l in self.file_lines if re.match(self.ray_regex, l)]

    def has_error(self):
        """Returns whether there is an error in the test file."""
        return self.error

    def get_rays(self):
        """Returns the array of rays to be shot into FenixBox."""
        return self.rays

def main():
    """Validate inputs, extract data and start simulation session."""
    debug_mode = False

    """Parse Command Line Arguments Input"""
    parser = argparse.ArgumentParser()
    parser.add_argument('design_filename', help='Path and/or Name of design file which specifies'
                        ' the size of grid and positions and types of mirrors.')
    parser.add_argument('test_filename', help='Path and/or Name of test file that lists the places'
                        ' in order a ray is fired in.')
    parser.add_argument('-d', help='Turns on debug mode to locate input errors.',action='store_true')
    args = parser.parse_args()

    debug_mode = args.d

    """Input Data Validation"""
    design_file = DesignFile(args.design_filename, debug_mode)
    test_file = TestFile(args.test_filename, debug_mode)
    design_file.validate()
    test_file.validate() 
    if design_file.has_error() or test_file.has_error():
        sys.exit(4)

    """Extract Data"""
    holes = design_file.get_holes()
    mirror_positions = design_file.get_mirrors()
    rays = test_file.get_rays()

    """Logical Validation to check if mirrors or rays are out of range"""
    for mirror in mirror_positions:
        if mirror[0] > holes or mirror[1] > holes:
            if debug_mode:    
                print(f'Mirror: {str(mirror)} out of range. FenixBox only has {holes} holes.')
            sys.exit(5)

    for ray in rays:
        if int(ray[1:-1]) > holes:
            if debug_mode:    
                print(f'Ray: {ray} out of range. FenixBox only has {holes} holes.')
            sys.exit(5)

    """Start Simulation Session"""
    session = Session(holes, mirror_positions, rays)
    session.start_simulation()

    """Terminate Program Upon Successful Completion"""
    sys.exit(0)


if __name__ == '__main__':
    """Parse and validate CLI arguments and call main function."""
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(6)