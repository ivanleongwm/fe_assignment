class Cell {
    constructor() {
        this.mirror = false;
        this.life = Infinity;
    }
    deductLife() {
        this.life -= 1;
        if (this.life === 0) {
            this.mirror = false;
            this.life = Infinity;
        }
    }
    isMirror() {
        return this.mirror;
    }
    setMirror() {
        this.mirror = true;
    }
    setLife(lifespan) {
        this.life = lifespan;
    }
}

class Beam {
    constructor(startCoordinates, length, grid) {
        this.startCoordinates = startCoordinates;
        this.end = false;
        this.collision = false;
        
        /** Initialise currRowIdx, currColIdx and currentDirection. */
        if (startCoordinates[0] === 'R' && startCoordinates.slice(-1) === '+') {
            this.currRowIdx = parseInt(startCoordinates.slice(1, -1)) - 1;
            this.currColIdx = 0;
            this.currentDirection = 'right';
        } else if (startCoordinates[0] === 'R' && startCoordinates.slice(-1) === '-') {
            this.currRowIdx = parseInt(startCoordinates.slice(1, -1)) - 1;
            this.currColIdx = length - 1;
            this.currentDirection = 'left';
        } else if (startCoordinates[0] === 'C' && startCoordinates.slice(-1) === '+') {
            this.currRowIdx = 0;
            this.currColIdx = parseInt(startCoordinates.slice(1, -1)) - 1;
            this.currentDirection = 'down';
        } else if (startCoordinates[0] === 'C' && startCoordinates.slice(-1) === '-') {
            this.currRowIdx = length - 1;
            this.currColIdx = parseInt(startCoordinates.slice(1, -1)) - 1;
            this.currentDirection = 'up';
        }

        /** Check if a mirror is right beside the beam at initial state. */
        if (startCoordinates[0] === 'C') {
            if (this.currColIdx !== 0) {
                let leftCell = grid[this.currRowIdx][this.currColIdx - 1];
                if (leftCell.isMirror()) {
                    this.end = true;
                    this.printOutput();
                    leftCell.deductLife();
                }
            }
            if (this.currColIdx !== (length - 1)) {
                let rightCell = grid[this.currRowIdx][this.currColIdx + 1];
                if (rightCell.isMirror()) {
                    this.end = true;
                    this.printOutput();
                    rightCell.deductLife();
                }
            }
        }
        if (startCoordinates[0] === 'R') {
            if (this.currRowIdx !== 0) {
                let topCell = grid[this.currRowIdx - 1][this.currColIdx];
                if (topCell.isMirror()) {
                    this.end = true;
                    this.printOutput();
                    topCell.deductLife();
                }
            }
            if (this.currRowIdx !== (length - 1)) {
                let bottomCell = grid[this.currRowIdx + 1][this.currColIdx];
                if (bottomCell.isMirror()) {
                    this.end = true;
                    this.printOutput();
                    bottomCell.deductLife();
                }
            }
        }
    }

    checkCollision(grid) {
        if (this.end) return;

        let currGridCell = grid[this.currRowIdx][this.currColIdx];
        if (currGridCell.isMirror()) {
            this.currentDirection = null;
            this.end = true;
            this.collision = true;
            this.printOutput();
            currGridCell.deductLife();
        }
    }

    checkMirror(grid, length) {
        if (this.end) return;

        let topRightMirror = false;
        let bottomRightMirror = false;
        let topLeftMirror = false;
        let bottomLeftMirror = false;

        if (this.currColIdx !== length - 1 && this.currRowIdx !== 0) {
            let topRightCell = grid[this.currRowIdx - 1][this.currColIdx + 1];
            topRightMirror = topRightCell.isMirror();
        }
        if (this.currColIdx !== length - 1 && this.currRowIdx !== length - 1) {
            let bottomRightCell = grid[this.currRowIdx + 1][this.currColIdx + 1];
            bottomRightMirror = bottomRightCell.isMirror();
        }
        if (this.currColIdx !== 0 && this.currRowIdx !== 0) {
            let topLeftCell = grid[this.currRowIdx - 1][this.currColIdx - 1];
            topLeftMirror = topLeftCell.isMirror();
        }
        if (this.currColIdx !== 0 && this.currRowIdx !== length - 1) {
            let bottomLeftCell = grid[this.currRowIdx + 1][this.currColIdx - 1];
            bottomLeftMirror = bottomLeftCell.isMirror();
        }

        if (this.currentDirection === 'right') {
            if (topRightMirror && bottomRightMirror) {
                this.currentDirection = 'left';
                topRightCell.deductLife();
                bottomRightCell.deductLife();
            } else if (topRightMirror) {
                this.currentDirection = 'down';
                topRightCell.deductLife();
            } else if (bottomRightMirror) {
                this.currentDirection = 'up';
                bottomRightCell.deductLife();
            }
        } else if (this.currentDirection === 'left') {
            if (topLeftMirror && bottomLeftMirror) {
                this.currentDirection = 'right';
                topLeftCell.deductLife();
                bottomLeftCell.deductLife();
            } else if (topLeftMirror) {
                this.currentDirection = 'down';
                topLeftCell.deductLife();
            } else if (bottomLeftMirror) {
                this.currentDirection = 'up';
                bottomLeftCell.deductLife();
            }
        } else if (this.currentDirection === 'up') {
            if (topLeftMirror && topRightMirror) {
                this.currentDirection = 'down';
                topLeftCell.deductLife();
                topRightCell.deductLife();
            } else if (topLeftMirror) {
                this.currentDirection = 'right';
                topLeftCell.deductLife();
            } else if (topRightMirror) {
                this.currentDirection = 'left';
                topRightCell.deductLife();
            }
        } else if (this.currentDirection === 'down') {
            if (bottomLeftMirror && bottomRightMirror) {
                this.currentDirection = 'up';
                bottomLeftCell.deductLife();
                bottomRightCell.deductLife();
            } else if (bottomLeftMirror) {
                this.currentDirection = 'right';
                bottomLeftCell.deductLife();
            } else if (bottomRightMirror) {
                this.currentDirection = 'left';
                bottomRightCell.deductLife();
            }
        }
    }

    checkEnd(length) {
        if (this.currentDirection === 'up' && this.currRowIdx === 0) {
            this.end = true;
            this.printOutput();
        } else if (this.currentDirection === 'right' && this.currColIdx === (length - 1)) {
            this.end = true;
            this.printOutput();
        } else if (this.currentDirection === 'down' && this.currRowIdx === (length - 1)) {
            this.end = true;
            this.printOutput();
        } else if (this.currentDirection === 'left' && this.currColIdx === 0) {
            this.end = true;
            this.printOutput();
        }
    }

    move() {
        if (this.end) return;

        if (this.currentDirection === 'right') {
            this.currColIdx += 1;
        } else if (this.currentDirection === 'left') {
            this.currColIdx -= 1;
        } else if (this.currentDirection === 'up') {
            this.currRowIdx -= 1;
        } else if (this.currentDirection === 'down') {
            this.currRowIdx += 1;
        }
    }

    printOutput() {
        if (this.collision) {
            console.log(`${this.startCoordinates} ->`);
        } else {
            console.log(`${this.startCoordinates} -> {${this.currRowIdx + 1},${this.currColIdx + 1}}`);
        }
    }

    isEnd() {
        return this.end;
    }
}


class Session {

    constructor(length, mirrorPositions, rays) {
        this.length = length;
        this.mirrorPositions = mirrorPositions;
        this.rays = rays;
        this.grid = this.createGrid();
    }

    createGrid() {
        let rows = [];
        for (let i = 0; i < this.length; i++) {
            let columns = [];
            for (let j = 0; j < this.length; j++) {
                columns.push(new Cell());
            }
            rows.push(columns);
        }

        for (let mirror of this.mirrorPositions) {
            let rowIdx = mirror[0] - 1;
            let colIdx = mirror[1] - 1;
            let cell = rows[rowIdx][colIdx];
            cell.setMirror();
            if (mirror.length === 3) {
                cell.setLife(mirror[2]);
            }
        }
        return rows;
    }

    startSimulation() {
        for (let ray of this.rays) {
            let beam = new Beam(ray, this.length, this.grid);
            while (!beam.isEnd()) {
                beam.checkCollision(this.grid);
                beam.checkMirror(this.grid, this.length);
                beam.checkEnd(this.length);
                beam.move();
            }
        }
    }
}