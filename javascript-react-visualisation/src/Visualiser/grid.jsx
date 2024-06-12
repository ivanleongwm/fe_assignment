import React, { useState, useEffect } from 'react';
import Node from './Node/Node'
import './grid.css'

const HOLES = 8;

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
            grid: getInitialGrid(HOLES)
        });
    }, [])

    const { grid } = state
    return (
        <div>
            <div className="grid">
                {grid.map((row, rowIdx) => {
                    return <div className='row' key={rowIdx}>
                        {row.map((node, nodeIdx) => {
                            const { row, col, isMirror, edge} = node;
                            return (
                                <Node
                                    key={nodeIdx}
                                    isMirror={isMirror}
                                    mirrorMode={state.mirrorMode}
                                    row={row}
                                    col={col}
                                    edge={edge}
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
            if ((row == 0 & col == 0) | (row == HOLES-1 & col == HOLES-1)
                | (row == 0 & col == HOLES-1) | (row == HOLES-1 & col == 0)
                ) {
                currentRow.push(createNode(col, row, false));
            }
            else if ((row == 0) | (col == 0) | (row == HOLES-1) | (col == HOLES-1)) {
                currentRow.push(createNode(col, row, true));
            } else {
                currentRow.push(createNode(col, row, false));
            }
            
        }
        grid.push(currentRow);
    }
    return grid;
};
const createNode = (col, row, edge) => {
    return {
        col,
        row,
        isMirror: false,
        edge: edge
    };
};
