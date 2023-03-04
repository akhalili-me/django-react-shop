import { Carousel } from 'react-bootstrap'


const _Carousel = ({items}) => {

    if (!items || !items.length ) {
        return <p>No items to display</p>
    }

    const carousel_items = items.map((item) =>
        <Carousel.Item key={item.id}>
            <img className='rounded d-block w-100' alt={item.name} src={item.image}/>
        </Carousel.Item>
    )

    return(
        <Carousel interval={null} variant="dark">
            {carousel_items} 
        </Carousel>
    )
}

export default _Carousel