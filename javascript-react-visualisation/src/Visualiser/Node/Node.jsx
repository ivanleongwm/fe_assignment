import React from 'react';
import './Node.css'

function Node({ row, col, isMirror, mirrorMode,edge,content }) {

    const handleClickCell = (event) => {
        if (!event.target.classList.contains('edge')
            & !event.target.classList.contains('outside')
            & !event.target.classList.contains('white-edge')
            ) {
            if (mirrorMode == 'Add Normal Mirror') {
                return addMirrorLife(event)
            } else if (mirrorMode == 'Remove Mirror') {
                return removeMirror(event)
            } else if (mirrorMode == 'Add Infinite Mirror') {
                return removeInfiniteMirror(event)
            }
        }
    }

    const addMirrorLife = (event) => {
        const cell = event.target
        cell.classList.add("node-mirror")
        if (cell.innerHTML < 1 | cell.innerHTML == '' | cell.innerHTML == '∞') {
            cell.innerHTML = 1
        } else {
            cell.innerHTML = parseInt(cell.innerHTML) + 1
        }
    }

    const removeMirror = (event) => {
        const cell = event.target
        cell.classList.remove("node-mirror");
        cell.innerHTML = '';
    }

    const removeInfiniteMirror = (event) => {
        const cell = event.target
        cell.classList.add("node-mirror")
        cell.innerHTML = '∞';
    }
 
    return (
        <div
            id={`node-${row}-${col}`}
            className={`node ${edge}`}
            onClick={handleClickCell}    
        >{content}</div>
    )
}

export default Node