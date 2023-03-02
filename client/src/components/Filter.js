import React, { useState, useCallback } from 'react'
import {ListGroup,InputGroup} from 'react-bootstrap';
import Form from 'react-bootstrap/Form';
import { useSearchParams } from 'react-router-dom'

const Filter = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  
  const [sort, setSort] = useState(searchParams.get('sort') || 'Default');
  const [minPrice, setMinPrice] = useState(searchParams.get('min') || 0);
  const [maxPrice, setMaxPrice] = useState(searchParams.get('max') || '');
  const [onlyAvailableProducts, setOnlyAvailableProducts] = useState(searchParams.get('has_selling_stock') || false);

  const handleSearchParamsChange = useCallback((event) => {
    const target = event.target;
    const name = target.name;
    const value = target.type === 'checkbox' ? target.checked : target.value;

    setSearchParams(prevSearchParams => {
      const allSearchParams = new URLSearchParams(prevSearchParams)

      if (!allSearchParams.has(name)) {
        allSearchParams.append(name, value);
      }else{
        allSearchParams.set(name, value);
      }
      
      return allSearchParams
    })

    if (name === 'sort') {
      setSort(value);
    } else if (name === 'min') {
      setMinPrice(value);
    } else if (name === 'max') {
      setMaxPrice(value);
    } else if(name === 'has_selling_stock')
      setOnlyAvailableProducts(value);

  }, [setSearchParams, setSort, setMinPrice, setMaxPrice,setOnlyAvailableProducts]);

  return (
    <ListGroup>
      <ListGroup.Item>
        <Form.Label>Sort by:</Form.Label>
        <Form.Select aria-label="Default" className='mb-1' onChange={handleSearchParamsChange} value={sort} name='sort'>
          <option>Default</option>
          <option value="popular">Most Liked</option>
          <option value="2">Price Ascending</option>
          <option value="3">Price Descending</option>
        </Form.Select>
      </ListGroup.Item>

      <ListGroup.Item>
        <InputGroup className="p-1 mb-1">
          <InputGroup.Text id="min-price-label">Min Price</InputGroup.Text>
          <Form.Control
            type="number"
            placeholder="0"
            value={minPrice}
            min={0}
            onChange={handleSearchParamsChange}
            name="min"
            aria-label="Minimum Price"
            aria-describedby="min-price-label"
          />
        </InputGroup>

        <InputGroup className="p-1">
          <InputGroup.Text id="max-price-label">Max Price</InputGroup.Text>
          <Form.Control
            type="number"
            placeholder="0"
            value={maxPrice}
            min={0}
            onChange={handleSearchParamsChange}
            name="max"
            aria-label="Maximum Price"
            aria-describedby="max-price-label"
          />
        </InputGroup>

      </ListGroup.Item>

      <ListGroup.Item>
        <Form.Check
          type="switch"
          id="custom-switch"
          label="Only available products"
          checked={onlyAvailableProducts}
          onChange={handleSearchParamsChange}
          name='has_selling_stock'
        />
      </ListGroup.Item>
    </ListGroup>
  )
}

export default Filter;
