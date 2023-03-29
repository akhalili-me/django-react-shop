import React, {useMemo, useCallback } from "react";
import Pagination from "react-bootstrap/Pagination";
import {useSearchParams } from "react-router-dom";
import { addNewParam } from "../../utility/queryParams";

const PAGE_RANGE_DISPLAYED = 3;

const generatePaginateItems = (currentPage, lastActivePage,handlePaginateItemClick) => {
  const paginateItems = [];

  for (
    let page = currentPage;
    page < currentPage + PAGE_RANGE_DISPLAYED;
    page++
  ) {
    if (page > 1 && page <= lastActivePage) {
      paginateItems.push(
        <Pagination.Item key={page} active={page === currentPage} onClick={() => handlePaginateItemClick(page)}>
          {page}
        </Pagination.Item>
      );
    }
  }

  return paginateItems;
};

const _Pagination = ({ count, paginateBy }) => {
  const [searchParams, setSearchParams] = useSearchParams();

  const lastActivePage = useMemo(
    () => Math.ceil(count / paginateBy),
    [count, paginateBy]
  );

  const currentPage = parseInt(searchParams.get("page")) || 1;

  const handleNext = useCallback(() => {
    addNewParam(setSearchParams, "page", currentPage + 1);
  }, [setSearchParams, currentPage]);

  const handlePrev = useCallback(() => {
    addNewParam(setSearchParams, "page", currentPage - 1);
  }, [setSearchParams, currentPage]);

  const handlePaginateItemClick = (page) => {
    addNewParam(setSearchParams, "page", page);
  }

  const paginateItems = generatePaginateItems(currentPage, lastActivePage, handlePaginateItemClick);

  return (
    <Pagination className="d-flex justify-content-center py-4">
      <Pagination.Prev disabled={currentPage === 1} onClick={handlePrev}>
        Prev
      </Pagination.Prev>

      <Pagination.Item key={1} active={currentPage === 1} onClick={() => handlePaginateItemClick(1)}>
        {1}
      </Pagination.Item>

      {paginateItems}

      <Pagination.Next
        disabled={currentPage === lastActivePage}
        onClick={handleNext}
      >
        Next
      </Pagination.Next>
    </Pagination>
  );
};

export default _Pagination;
