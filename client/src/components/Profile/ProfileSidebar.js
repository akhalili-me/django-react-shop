import React, { useState } from "react";
import { ListGroup, InputGroup, Col, Row } from "react-bootstrap";
import { Link } from "react-router-dom";

const ProfileSidebar = ({ user }) => {
  return (
    <ListGroup>
      <ListGroup.Item>Amirreza Khalili Amir@gmail.com</ListGroup.Item>

      <Link to={"/profile/orders"}>
        <ListGroup.Item action>Orders</ListGroup.Item>
      </Link>
      <Link to={"/profile/comments"}>
        <ListGroup.Item action>Comments</ListGroup.Item>
      </Link>
      <Link to={"/profile/address"}>
        <ListGroup.Item action>Addresses</ListGroup.Item>
      </Link>
    </ListGroup>
  );
};

export default ProfileSidebar;
