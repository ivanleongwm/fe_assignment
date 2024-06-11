if __name__ == '__main__':
    import sys
    import os
    import re
    import time
    import logging
    import argparse
    from impl1 import Session

def validate_parse_design_file(lines):
    pattern = r'^\d\s\d\s?\d*$'
    noise = [l for l in lines if not re.match(pattern,l)]
    print(noise)

def read_design_file(designFilepath):
    """Parse design file and return length and mirror position."""
    try:
        with open(designFilepath) as file:

            lines = file.read().splitlines()

            validate_parse_design_file(lines)

            # Remove comment / invalid lines
            data_lines = [l for l in lines if l.replace(" ","").isdigit()]
            # Retrieve grid length
            length = int(data_lines.pop(0))
            # Retrieve mirror positions
            mirror_positions = []
            for mirrors in data_lines:
                mirror_positions.append([int(mirror) for mirror in mirrors.split()])

        return length, mirror_positions
    except IOError:
        print(f'Could not read file: {designFilepath}. Please check file name or directory.')
        sys.exit(3)


def validate_parse_test_file(lines):
    """Check test file for invalid line(s) other than comments, spaces or rays."""
    pattern = r'^[CR][1-9][0-9]*[+-]$'    #need to exclude c0+ as 0 is not a valid row
    error = False
    for idx, line in enumerate(lines):
        if (not re.match(pattern,line)) and (line != '') and (not line.startswith('#')):
            error = True
            print(f'Invalid Ray: "{line}" on Line {idx + 1} of testfile.')
    if not error:
        rays = [l for l in lines if re.match(pattern,line)]
        return rays   
    else:
        sys.exit(5) 


def read_test_file(testFilepath):
    """Parse test file and return an array of places a ray is fired."""
    try:
        with open(testFilepath) as file:
            lines = file.read().splitlines()
            rays = validate_parse_test_file(lines)
            return rays
    except IOError:
        print(f'Could not read file: {testFilepath}. Please check file name or directory.')
        sys.exit(4)

def main():
    """Validate inputs and start simulation session."""
    #level = logging.DEBUG
    #fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    #logging.basicConfig(level=level, format=fmt)

    parser = argparse.ArgumentParser()
    parser.add_argument('designFilepath',help='Path to design file which specifies \
                        the size of grid and positions and types of mirrors.')
    parser.add_argument('testFilepath',help='Path to test file that lists the places \
                        in order a ray is fired in.')
    args = parser.parse_args()

    designFilepath = args.designFilepath
    testFilepath = args.testFilepath
    
    length, mirror_positions = read_design_file(designFilepath)
    rays = read_test_file(testFilepath)

    start = time.perf_counter()
    session = Session(length, mirror_positions, rays)
    session.start_simulation()
    end = time.perf_counter()
    print(end-start)


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