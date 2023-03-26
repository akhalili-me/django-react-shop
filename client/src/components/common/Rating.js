import React from 'react'

const Rating = ({value,text}) => {
    const stars = []
    for (let i = 1; i <= 5; i++) {
        let star = <span>
        <i className={
            value >= i ? 'fa-solid fa-star': value >=(i-0.5) ? 'fas fa-star-half-alt': 'fa-regular fa-star'
        }
        >
        </i>
        </span>
        stars.push(star)
    } 

    return (
        <div className='star_color'>{stars} 
            <span className='regular_color'>{text}</span>
        </div>
    )
}

export default Rating



