import React from 'react';
import './Node.css'

function Node(props) {
    const { row, col, isFinish, isStart } = props
    const extraClassName = isFinish ? 'node-finish' : isStart ? 'node-start' : '';
    return (
        <div
            id={`node-${row}-${col}`}
            className={`node ${extraClassName}`}></div>
    )
}

export default Node