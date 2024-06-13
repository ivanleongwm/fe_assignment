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

   const checkEnd = (curr_row,curr_col,currentDirection, length) => {
        if (currentDirection === 'up' && curr_row === 2) {
            return true
        } else if (currentDirection === 'right' && curr_col === (length + 1)) {
            return true
        } else if (currentDirection === 'down' && curr_row === (length + 1)) {
            return true
        } else if (currentDirection === 'left' && curr_col === 2) {
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

    const animate = (curr_row,curr_col,direction) => {
        wipe_visited()
        for (let i = 0; i < 6; i++ ) {
            setTimeout(() => {
                document.getElementById(`${String(curr_row+i)}-${String(curr_col)}`).className = 'node node-visited';
            }, 10*i*3);
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
