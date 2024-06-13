import React, { useState, useEffect } from 'react';
import Node from './Node/Node'
import './grid.css'

const HOLES = 8

export default function Grid() {
    const [state, setState] = useState({
        grid: [],
        mirrorMode: 'Add Normal Mirror',
        rayStart: '',
        rayDirection: ''
    });

    const updateRayStart = (event) => {
        let direction = ''
        let curr_row = 0
        let curr_col = 0
        if (event.target.classList.contains('edge')) {
            const cell_id = event.target.id.split('-').map(function(item){
                return parseInt(item)
            })
            if (cell_id[1]==1){
                direction = 'right'
                curr_row = cell_id[0]
                curr_col = cell_id[1]+1
            } else if (cell_id[1]==HOLES+2) {
                direction = 'left'
                curr_row = cell_id[0]
                curr_col = cell_id[1]-1
            } else if (cell_id[0]==1) {
                direction = 'down'
                curr_row = cell_id[0]+1
                curr_col = cell_id[1]
            } else if (cell_id[0]==HOLES+2) {
                direction = 'up'
                curr_row = cell_id[0]-1
                curr_col = cell_id[1]
            }
            setState(state=>({
                ...state,
                rayStart: [curr_row,curr_col],
                rayDirection: direction
            }))
            console.log(cell_id,direction)
            animate(curr_row,curr_col,direction)
        }
    }

    

    const changeMirrorMode = (event) => {
        setState(state=>({
            ...state,
            mirrorMode: event.target.innerHTML
        }))
        console.log(state.mirrorMode)
    }

   const checkEnd = (curr_row,curr_col,currentDirection) => {
        if (currentDirection == 'up' & curr_row == 1) {
            return true
        } else if (currentDirection == 'right' & curr_col == (HOLES + 2)) {
            return true
        } else if (currentDirection == 'down' & curr_row == (HOLES + 2)) {
            return true
        } else if (currentDirection == 'left' & curr_col == 1) {
            return true
        }
    }

    const wipe_visited = () => {
        for (let i=0; i < HOLES+2; i++) {
            for (let y=0; y < HOLES+2; y++) {
                document.getElementById(`${String(i)}-${String(y)}`).classList.remove('node-visited');
            }
        }
    }

    const move = (curr_row,curr_col,currentDirection) => {
        if (currentDirection === 'right') {
            return [curr_row,curr_col+1]
        } else if (currentDirection === 'left') {
            return [curr_row,curr_col-1]
        } else if (currentDirection === 'up') {
            return [curr_row-1,curr_col]
        } else if (currentDirection === 'down') {
            return [curr_row+1,curr_col]
        }
    }

    const checkMirror = (curr_row, curr_col, length, currentDirection) => {

        let topRightMirror = false;
        let bottomRightMirror = false;
        let topLeftMirror = false;
        let bottomLeftMirror = false;
        let topLeftCell = document.getElementById(`${String(curr_row - 1)}-${String(curr_col - 1)}`);
        let bottomLeftCell = document.getElementById(`${String(curr_row + 1)}-${String(curr_col - 1)}`);
        let topRightCell = document.getElementById(`${String(curr_row - 1)}-${String(curr_col + 1)}`);
        let bottomRightCell = document.getElementById(`${String(curr_row + 1)}-${String(curr_col + 1)}`);
        
        if (curr_col < length + 2 & curr_row > 2) {
            let topRightCell = document.getElementById(`${String(curr_row - 1)}-${String(curr_col + 1)}`)
            topRightMirror = topRightCell.classList.contains('node-mirror')
        }
        if (curr_col < length + 2 & curr_row < length + 2) {
            let bottomRightCell = document.getElementById(`${String(curr_row + 1)}-${String(curr_col + 1)}`)
            bottomRightMirror = bottomRightCell.classList.contains('node-mirror')
        }
        if (curr_col > 2 & curr_row > 2) {
            let topLeftCell =  document.getElementById(`${String(curr_row - 1)}-${String(curr_col - 1)}`)
            topLeftMirror = topLeftCell.classList.contains('node-mirror')
        }
        if (curr_col > 2 & curr_row < length + 2) {
            let bottomLeftCell = document.getElementById(`${String(curr_row + 1)}-${String(curr_col - 1)}`)
            bottomLeftMirror = bottomLeftCell.classList.contains('node-mirror')
        }

        console.log(topRightMirror,bottomRightMirror,topLeftMirror,bottomLeftMirror)

        if (currentDirection === 'right') {
            if (topRightMirror && bottomRightMirror) {
                if (topRightCell.innerHTML != '∞') {
                    topRightCell.innerHTML = parseInt(topRightCell.innerHTML) - 1
                    removeEmptyMirror(topRightCell)
                } 
                if (bottomRightCell.innerHTML != '∞'){
                    bottomRightCell.innerHTML = parseInt(bottomRightCell.innerHTML) - 1
                    removeEmptyMirror(bottomRightCell)
                }
                return 'left'
            } else if (topRightMirror) {
                if (topRightCell.innerHTML != '∞') {
                    topRightCell.innerHTML = parseInt(topRightCell.innerHTML) - 1
                    removeEmptyMirror(topRightCell)
                }
                return 'down'
            } else if (bottomRightMirror) {
                if (bottomRightCell.innerHTML != '∞'){
                    bottomRightCell.innerHTML = parseInt(bottomRightCell.innerHTML) - 1
                    removeEmptyMirror(bottomRightCell)
                }
                return 'up'
            }} else if (currentDirection === 'left') {
                if (topLeftMirror && bottomLeftMirror) {
                    if (topLeftCell.innerHTML != '∞') {
                        topLeftCell.innerHTML = parseInt(topLeftCell.innerHTML) - 1
                        removeEmptyMirror(topLeftCell)
                    }
                    if (bottomLeftCell.innerHTML != '∞'){
                        bottomLeftCell.innerHTML = parseInt(bottomLeftCell.innerHTML) - 1
                        removeEmptyMirror(bottomLeftCell)
                    }
                    return 'right'
                } else if (topLeftMirror) {
                    if (topLeftCell.innerHTML != '∞') {
                        topLeftCell.innerHTML = parseInt(topLeftCell.innerHTML) - 1
                        removeEmptyMirror(topLeftCell)
                    }
                    return 'down'
                } else if (bottomLeftMirror) {
                    if (bottomLeftCell.innerHTML != '∞') {
                        bottomLeftCell.innerHTML = parseInt(bottomLeftCell.innerHTML) - 1
                        removeEmptyMirror(bottomLeftCell)
                    }
                    return 'up'
                }
            } else if (currentDirection === 'up') {
                if (topLeftMirror && topRightMirror) {
                    if (topLeftCell.innerHTML != '∞') {
                        topLeftCell.innerHTML = parseInt(topLeftCell.innerHTML) - 1
                        removeEmptyMirror(topLeftCell)
                    }
                    if (topRightCell.innerHTML != '∞'){
                        topRightCell.innerHTML = parseInt(topRightCell.innerHTML) - 1
                        removeEmptyMirror(topRightCell)
                    }
                    return 'down';
                } else if (topLeftMirror) {
                    if (topLeftCell.innerHTML != '∞') {
                        topLeftCell.innerHTML = parseInt(topLeftCell.innerHTML) - 1
                        removeEmptyMirror(topLeftCell)
                    }
                    return 'right'
                } else if (topRightMirror) {
                    if (topRightCell.innerHTML != '∞') {
                        topRightCell.innerHTML = parseInt(topRightCell.innerHTML) - 1
                        removeEmptyMirror(topRightCell)
                    }
                    return 'left'
                }
            } else if (currentDirection === 'down') {
                if (bottomLeftMirror && bottomRightMirror) {
                    if (bottomLeftCell.innerHTML != '∞') {
                        bottomLeftCell.innerHTML = parseInt(bottomLeftCell.innerHTML) - 1
                        removeEmptyMirror(bottomLeftCell)
                    }
                    if (bottomRightCell.innerHTML != '∞'){
                        bottomRightCell.innerHTML = parseInt(bottomRightCell.innerHTML) - 1
                        removeEmptyMirror(bottomRightCell)
                    }
                    return 'up'
                } else if (bottomLeftMirror) {
                    if (bottomLeftCell.innerHTML != '∞') {
                        bottomLeftCell.innerHTML = parseInt(bottomLeftCell.innerHTML) - 1
                        removeEmptyMirror(bottomLeftCell)
                    }
                    return 'right'
                } else if (bottomRightMirror) {
                    if (bottomRightCell.innerHTML != '∞') {
                        bottomRightCell.innerHTML = parseInt(bottomRightCell.innerHTML) - 1
                        removeEmptyMirror(bottomRightCell)
                    }
                    return 'left'
                }
            }
        
        return currentDirection

    }

    const checkCollision = (new_row,new_col) => {
        let current_cell = document.getElementById(`${String(new_row)}-${String(new_col)}`)
        if (current_cell.classList.contains('node-mirror')) {
            if (current_cell.innerHTML != '∞' ) {
                current_cell.innerHTML = parseInt(current_cell.innerHTML) - 1
                removeEmptyMirror(current_cell)
                return true
            } else {
                return true
            }

            
        } else {
            return false
        }
    }

    const removeEmptyMirror = (cell) => {
        if (cell.innerHTML != '∞' && parseInt(cell.innerHTML)==0){
            cell.classList.remove('node-mirror');
            cell.innerHTML = '';
        }
    } 

    async function animate(curr_row,curr_col,direction) {
        wipe_visited()
        let new_row = curr_row;
        let new_col = curr_col;
        let new_direction = direction;
        let start_sides_mirror = false

        if (new_direction == 'up' | new_direction == 'down') {
            if (new_col !== 1) {
                let leftCell = document.getElementById(`${String(new_row)}-${String(new_col - 1)}`)
                if (leftCell.classList.contains('node-mirror')) {
                    if (leftCell.innerHTML != '∞'){
                        leftCell.innerHTML = parseInt(leftCell.innerHTML) - 1
                        removeEmptyMirror(leftCell)
                    }
                    document.getElementById(`${String(new_row)}-${String(new_col)}`).className = 'node node-visited';
                    start_sides_mirror = true
                }
            }
            if (new_col !== (HOLES + 1)) {
                let rightCell = document.getElementById(`${String(new_row)}-${String(new_col + 1)}`)
                if (rightCell.classList.contains('node-mirror')) {
                    if (rightCell.innerHTML != '∞'){
                        rightCell.innerHTML = parseInt(rightCell.innerHTML) - 1
                        removeEmptyMirror(rightCell)
                    }
                    document.getElementById(`${String(new_row)}-${String(new_col)}`).className = 'node node-visited';
                    start_sides_mirror = true
                }
            }
        } 
        if (new_direction == 'left' | new_direction == 'right') {
            if (new_row !== 1) {
                let topCell = document.getElementById(`${String(new_row-1)}-${String(new_col)}`)
                if (topCell.classList.contains('node-mirror')) {
                    if (topCell.innerHTML != '∞'){
                        topCell.innerHTML = parseInt(topCell.innerHTML) - 1
                        removeEmptyMirror(topCell)
                    }
                    document.getElementById(`${String(new_row)}-${String(new_col)}`).className = 'node node-visited';
                    start_sides_mirror = true
                }
            }
            if (new_row !== HOLES + 1) {
                let bottomCell = document.getElementById(`${String(new_row+1)}-${String(new_col)}`)
                if (bottomCell.classList.contains('node-mirror')) {
                    if (bottomCell.innerHTML != '∞'){
                        bottomCell.innerHTML = parseInt(bottomCell.innerHTML) - 1
                        removeEmptyMirror(bottomCell)
                    }
                    document.getElementById(`${String(new_row)}-${String(new_col)}`).className = 'node node-visited';
                    start_sides_mirror = true
                }
            }
        }
        if (start_sides_mirror) {
            return 0
        }


        for (let i = 0; i < Infinity; i++ ) {

            document.getElementById(`${String(new_row)}-${String(new_col)}`).className = 'node node-visited';
            await new Promise(r => setTimeout(r, 200));
            
            new_direction = checkMirror(new_row,new_col,HOLES,new_direction);
           

            [new_row, new_col] = move(new_row,new_col,new_direction);
      

            console.log("NEW",new_row,new_col);     
            console.log(direction,checkEnd(new_row,new_col,direction))
            if (checkEnd(new_row,new_col,new_direction) | checkCollision(new_row,new_col)) {
                break;
            }
        }
    }

    useEffect(() => {
        setState({
            grid: getInitialGrid(HOLES+4) // add 2 holes for edges
        });
    }, [])

    const { grid } = state
    return (
        <div>
            <div className="grid">
                {grid.map((row, rowIdx) => {
                    return <div className='row' key={rowIdx}>
                        {row.map((node, nodeIdx) => {
                            const { row, col, isMirror, edge, content} = node;
                            return (
                                <Node
                                    key={nodeIdx}
                                    isMirror={isMirror}
                                    mirrorMode={state.mirrorMode}
                                    row={row}
                                    col={col}
                                    edge={edge}
                                    content={content}
                                    updateRayStart={updateRayStart}
                                    animate={animate}
                                    />
                            );
                        })}
                    </div>
                })}
                <p>FenixBox Description</p>
                <button onClick={changeMirrorMode}>Remove Mirror</button>
                <button onClick={changeMirrorMode}>Add Normal Mirror</button>
                <button onClick={changeMirrorMode}>Add Infinite Mirror</button>
                <button onClick={changeMirrorMode}>Shoot Ray</button>
            </div>
        </div>
    )
}

const getInitialGrid = (HOLES) => {
    const grid = [];
    for (let row = 0; row < HOLES; row++) {
        const currentRow = [];
        for (let col = 0; col < HOLES; col++) {
            if ( (row == 1 & col == 0) | (row == 0 & col == 1) 
                | (row == HOLES-2 & col == HOLES-1) | (row == HOLES-1 & col == HOLES-2)
                | (row == 1 & col == HOLES-1) | (row == 0 & col == HOLES-2) 
                | (row == HOLES-2 & col == 0) | (row == HOLES-1 & col == 1) 
                | (row == 0 & col == 0) | (row == 0 & col == HOLES-1) 
                | (row == HOLES-1 & col == 0) | (row == HOLES-1 & col == HOLES-1) 
                ) {
                currentRow.push(createNode(col, row, 'outside'));
            }
            else if ((row == 1 & col == 1)| (row == HOLES-2 & col == HOLES-2)
                     |(row == 1 & col == HOLES-2) | (row == HOLES-2 & col == 1)) {
                currentRow.push(createNode(col, row, 'white-edge'));
            }
            else if ((row == 1) | (col == 1) | (row == HOLES-2) | (col == HOLES-2)) {
                currentRow.push(createNode(col, row, 'edge'));
            }
            else if ((col == 0)|(col == HOLES-1)) {
                currentRow.push(createNode(col, row, 'outside',row-1));
            } else if ((row == 0)|(row == HOLES-1)) {
                currentRow.push(createNode(col, row, 'outside',col-1));
            }
            else {
                currentRow.push(createNode(col, row, 'inside'));
            }
            
        }
        grid.push(currentRow);
    }
    return grid;
};
const createNode = (col, row, edge, content) => {
    return {
        col,
        row,
        isMirror: false,
        edge: edge,
        content: content,
    };
};
