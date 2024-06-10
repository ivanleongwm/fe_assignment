import React from 'react';
import './Node.css'

function Node({ row, col, isMirror }) {
    
    const extraClassName = isMirror ? 'node-mirror' : '';
    return (
        <div
            id={`node-${row}-${col}`}
            className={`node ${extraClassName}`}></div>
    )
}

export default Node