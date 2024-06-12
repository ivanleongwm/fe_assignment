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
                            const { row, col, isMirror} = node;
                            return (
                                <Node
                                    key={nodeIdx}
                                    isMirror={isMirror}
                                    mirrorMode={state.mirrorMode}
                                    row={row}
                                    col={col}
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
            currentRow.push(createNode(col, row));
        }
        grid.push(currentRow);
    }
    return grid;
};
const createNode = (col, row) => {
    return {
        col,
        row,
        isMirror: false
    };
};
