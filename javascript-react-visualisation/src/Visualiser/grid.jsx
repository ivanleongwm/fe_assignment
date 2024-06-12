import React, { useState, useEffect } from 'react';
import Node from './Node/Node'
import './grid.css'

const START_NODE_ROW = 5;
const START_NODE_COL = 2;
const FINISH_NODE_ROW = 10;
const FINISH_NODE_COL = 45;
const HOLES = 8;

export default function Grid() {
    const [state, setState] = useState({
        grid: []
    });

    useEffect(() => {
        setState({
            grid: getInitialGrid(HOLES)
        });
    }, [])

    const { grid, mouseIsPressed } = state
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
                                    row={row}
                                    col={col} />
                            );
                        })}
                    </div>
                })}
                <p>FenixBox Description</p>
                <Node />
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
        isMirror: false,
    };
};
