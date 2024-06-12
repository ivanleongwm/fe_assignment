import React, { useState, useEffect } from 'react';
import Node from './Node/Node'
import './grid.css'

const HOLES = 8

export default function Grid() {
    const [state, setState] = useState({
        grid: [],
        mirrorMode: 'Add Normal Mirror'
    });

    const changeMirrorMode = (event) => {
        setState(state=>({
            ...state,
            mirrorMode: event.target.innerHTML
        }))
        console.log(state.mirrorMode)
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
                                    />
                            );
                        })}
                    </div>
                })}
                <p>FenixBox Description</p>
                <button onClick={changeMirrorMode}>Remove Mirror</button>
                <button onClick={changeMirrorMode}>Add Normal Mirror</button>
                <button onClick={changeMirrorMode}>Add Infinite Mirror</button>
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
