if __name__ == '__main__':
    import sys
    import os
    import re
    from impl1 import Session

def parse_design_file(designFilepath):
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
    with open(testFilepath) as file:
        lines = file.read().splitlines()
        # Remove comment / invalid lines 
        pattern = r'^[CR][1-9][+-]$'
        rays = [l for l in lines if re.match(pattern,l)]
        return rays

def main(inputs):
    
    # 
    if len(inputs) == 2:
        designFilepath = inputs[0]
        testFilepath = inputs[1]
        length, mirror_positions = parse_design_file(designFilepath)
        rays = parse_test_file(testFilepath)
        session = Session(length, mirror_positions, rays)
        session.start_simulation()

    else:
        sys.exit(2)


    #config_logger()
    #logger.info("Configured logger")

    #consumer = XXX
    #conumer.run()


if __name__ == '__main__':
    
    # parse and verify the input (abstract input validation with another function or file)
    try:
        '''INSERT INPUT VALIDATION'''
        inputs = sys.argv[1:]
        main(inputs)
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            sys.exit()
        except SystemExit:
            os._exit(0)