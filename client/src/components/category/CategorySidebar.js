import { useMemo } from "react";
import { Accordion } from "react-bootstrap";
import { useSelector } from "react-redux";
import ListGroup from "react-bootstrap/ListGroup";
import { LinkContainer } from "react-router-bootstrap";
const CategorySidebar = ({ closeSidebar }) => {
  const categories = useSelector((state) => state.category.categories);

  const parentCategories = categories.filter(
    (category) => category.parent === null
  );

  const getChildCategories = useMemo(() => {
    return (id) => categories.filter((category) => category.parent === id);
  }, [categories]);

  return (
    <Accordion flush>
      {parentCategories.map((parentCategory) => {
        return (
          <Accordion.Item eventKey={parentCategory.id} key={parentCategory.id}>
            <Accordion.Header>{parentCategory.name}</Accordion.Header>
            <Accordion.Body>
              <ListGroup variant="flush">
                {getChildCategories(parentCategory.id).map((childCategory) => {
                  return (
                    <LinkContainer
                      to={`/product/filter/${childCategory.id}`}
                      onClick={closeSidebar}
                    >
                      <ListGroup.Item action>
                        {childCategory.name}
                      </ListGroup.Item>
                    </LinkContainer>
                  );
                })}
              </ListGroup>
            </Accordion.Body>
          </Accordion.Item>
        );
      })}
    </Accordion>
  );
};

export default CategorySidebar;
