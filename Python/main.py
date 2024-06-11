if __name__ == '__main__':
    import sys
    import os
    import re
    import time
    import logging
    import argparse
    from impl1 import Session

class File():
    def __init__(self,filename):
        self.filename = filename

    def get_file_lines(self):
        try:
            with open(self.filename) as file:
                lines = file.read().splitlines()
                return lines
        except IOError:
            print(f'Could not read file: {self.filename}. Please check file name or directory.')
            sys.exit(4)



class DesignFile(File):
    def __init__(self,filename):
        super().__init__(filename)
        self.file_lines = self.get_file_lines()
        self.mirror_regex = r'^[1-9][0-9]*\s[1-9][0-9]*\s?([1-9][0-9]*)*$'
        self.holes = None
        self.mirrors = self.parse_mirrors()
        self.error = False
    
    def validate(self):
        self.check_holes_error()
        self.check_mirror_error()

    def check_holes_error(self):
        for line in self.file_lines:
            if re.match(self.mirror_regex,line):
                print('Number of holes in FenixBox should be on first uncommented line.')
                self.error = True
                return None
            elif line.isdigit():
                self.holes = int(line)
                return None
        print('Number of holes in FenixBox missing from design file.')
        self.error = True

    def check_mirror_error(self):
        if self.holes:
            mirror_index = self.file_lines.index(str(self.holes)) + 1
        else:
            mirror_index = 0
        mirror_lines = self.file_lines[mirror_index:]
        for idx, line in enumerate(mirror_lines):
            if (not re.match(self.mirror_regex,line)) and (line != '') and (not line.startswith('#')):
                self.error = True
                print(f'Invalid Mirror: "{line}" on Line {idx + mirror_index + 1} of design file.')

    def parse_mirrors(self):
        mirrors = []
        for line in self.file_lines:    
            if re.match(self.mirror_regex,line):
                mirrors.append([int(mirror) for mirror in line.split()])
        return mirrors

    def has_error(self):
        return self.error

    def get_holes(self):
        return self.holes
    
    def get_mirrors(self):
        return self.mirrors
    
class TestFile(File):
    def __init__(self,filename):
        super().__init__(filename)
        self.file_lines = self.get_file_lines()
        self.ray_regex = r'^[CR][1-9][0-9]*[+-]$'
        self.rays = self.parse_rays()
        self.error = False

    def validate(self):
        self.check_rays_error()

    def check_rays_error(self):
        for idx, line in enumerate(self.file_lines):
            if (not re.match(self.ray_regex,line)) and (line != '') and (not line.startswith('#')):
                self.error = True
                print(f'Invalid Ray: "{line}" on Line {idx + 1} of testfile.')

    def parse_rays(self):
        return [l for l in self.file_lines if re.match(self.ray_regex,l)]

    def has_error(self):
        return self.error

    def get_rays(self):
        return self.rays

def main():
    """Validate inputs and start simulation session."""
    #level = logging.DEBUG
    #fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    #logging.basicConfig(level=level, format=fmt)

    parser = argparse.ArgumentParser()
    parser.add_argument('design_filename',help='Path to design file which specifies \
                        the size of grid and positions and types of mirrors.')
    parser.add_argument('test_filename',help='Path to test file that lists the places \
                        in order a ray is fired in.')
    args = parser.parse_args()

    design_file = DesignFile(args.design_filename)
    test_file = TestFile(args.test_filename)

    design_file.validate()
    test_file.validate() 

    if design_file.has_error() or test_file.has_error():
        sys.exit(3)
    else:
        holes = design_file.get_holes()
        mirror_positions = design_file.get_mirrors()
        rays = test_file.get_rays()

    #start = time.perf_counter()
    session = Session(holes, mirror_positions, rays)
    session.start_simulation()
    #end = time.perf_counter()
    #print(end-start)


if __name__ == '__main__':
    """Parse and validate CLI arguments and call main function."""
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            sys.exit()
        except SystemExit:
            os._exit(0)