if __name__ == '__main__':
    import sys
    import os
    import re
    import time
    import logging
    from impl1 import Session


def parse_design_file(designFilepath):
    """Parse design file and return length and mirror position."""
    with open(designFilepath) as file:
        lines = file.read().splitlines()
        # Remove comment / invalid lines
        data_lines = [l for l in lines if l.replace(" ","").isdigit()]
        # Retrieve grid length
        length = int(data_lines.pop(0))
        # Retrieve mirror positions
        mirror_positions = []
        for mirrors in data_lines:
            mirror_positions.append([int(mirror) for mirror in mirrors.split()])

    return length, mirror_positions


def parse_test_file(testFilepath):
    """Parse test file and return an array of places a ray is fired."""
    with open(testFilepath) as file:
        lines = file.read().splitlines()
        # Remove comment / invalid lines 
        pattern = r'^[CR][0-9]+[+-]$'    #need to exclude c0+ as 0 is not a valid row
        rays = [l for l in lines if re.match(pattern,l)]
        return rays


def main(inputs):
    """Validate inputs and start simulation session."""
    level = logging.DEBUG
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=fmt)

    if len(inputs) == 2:
        designFilepath = inputs[0]
        testFilepath = inputs[1]
        length, mirror_positions = parse_design_file(designFilepath)
        rays = parse_test_file(testFilepath)

        start = time.perf_counter()
        session = Session(length, mirror_positions, rays)
        session.start_simulation()
        end = time.perf_counter()
        print(end-start)

    else:
        sys.exit(2)


if __name__ == '__main__':
    """Parse and validate CLI arguments and call main function."""
    try:
        inputs = sys.argv[1:]
        main(inputs)
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            sys.exit()
        except SystemExit:
            os._exit(0)