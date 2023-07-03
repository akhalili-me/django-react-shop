import { useMemo } from "react";
import { Accordion } from "react-bootstrap";
import { useSelector } from "react-redux";
import ListGroup from "react-bootstrap/ListGroup";
import { LinkContainer } from "react-router-bootstrap";
import Loader from "../common/Loader";
import Message from "../common/Message";
const CategorySidebar = ({ closeSidebar }) => {
  const categoryList = useSelector((state) => state.category);
  const { categories, loading, error } = categoryList;

  const parentCategories = categories.filter(
    (category) => category.parent === null
  );

  const getChildCategories = useMemo(() => {
    return (id) => categories.filter((category) => category.parent === id);
  }, [categories]);

  return (
		<>
			{loading ? (
				<Loader />
			) : error ? (
				<Message variant={"danger"} message={error} />
			) : (
				<Accordion flush>
					{parentCategories.map((parentCategory) => {
						return (
							<Accordion.Item
								eventKey={parentCategory.id}
								key={parentCategory.id}
							>
								<Accordion.Header>
									{parentCategory.name}
								</Accordion.Header>
								<Accordion.Body>
									<ListGroup variant="flush">
										{getChildCategories(
											parentCategory.id
										).map((childCategory) => {
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
			)}
		</>
  );
};

export default CategorySidebar;
