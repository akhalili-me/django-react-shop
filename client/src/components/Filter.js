import React, { useState, useCallback } from "react";
import { ListGroup, InputGroup, Button } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import { useSearchParams } from "react-router-dom";
import { addArrayOfParamsToUrl } from "../utility/queryParams";

const Filter = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const [sort, setSort] = useState(searchParams.get("sort") || "");
  const [minPrice, setMinPrice] = useState(searchParams.get("min") || 0);
  const [maxPrice, setMaxPrice] = useState(searchParams.get("max") || 0);
  const [hasSellingStock, setHasSellingStock] = useState(
    searchParams.get("has_selling_stock") || ""
  );

  const handleSearchParamsChange = useCallback(
    (event) => {
      const target = event.target;
      const name = target.name;
      const value = target.type === "checkbox" ? target.checked : target.value;

      if (name === "sort") {
        setSort(value);
      } else if (name === "min") {
        setMinPrice(value);
      } else if (name === "max") {
        setMaxPrice(value);
      } else if (name === "has_selling_stock") setHasSellingStock(value);
    },
    [setSort, setMinPrice, setMaxPrice, setHasSellingStock]
  );

  const applyFilters = () => {
    let params = [];

    if (sort !== "") {
      params.push({ name: "sort", value: sort });
    }

    if (minPrice !== 0) {
      params.push({ name: "min", value: minPrice });
    }

    if (maxPrice !== 0) {
      params.push({ name: "max", value: maxPrice });
    }

    if (hasSellingStock !== "") {
      params.push({ name: "has_selling_stock", value: hasSellingStock });
    }

    addArrayOfParamsToUrl(setSearchParams, params);
  };

  return (
    <ListGroup>
      <ListGroup.Item>
        <Form.Label>Sort by:</Form.Label>
        <Form.Select
          aria-label="Default"
          className="mb-1"
          onChange={handleSearchParamsChange}
          value={sort}
          name="sort"
        >
          <option value="default">Default</option>
          <option value="newest">Newest</option>
          <option value="bestselling">Bestselling</option>
          <option value="popular">Most Liked</option>
          <option value="cheapest">Cheapest</option>
          <option value="most_expensive">Most Expensive</option>
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
            min={minPrice}
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
          checked={hasSellingStock}
          onChange={handleSearchParamsChange}
          name="has_selling_stock"
        />
      </ListGroup.Item>
      <ListGroup.Item>
        <Button onClick={() => applyFilters()} className="col-12">
          Apply Filters
        </Button>
      </ListGroup.Item>
    </ListGroup>
  );
};

export default Filter;
