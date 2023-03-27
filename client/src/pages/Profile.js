import React from "react";
import { Col, Row } from "react-bootstrap";
import ProfileSidebar from "../components/profile/ProfileSidebar";
import { Routes, Route } from "react-router-dom";
import Orders from "../components/profile/Orders";
import Comments from "../components/profile/Comments";

const Profile = () => {
  return (
    <Row>
      <Col md={4}>
        <ProfileSidebar />
      </Col>
      <Col md={8}>
        <Routes>
          <Route path="/orders" element={<Orders />} />
          <Route path="/comments" element={<Comments />} />
        </Routes>
      </Col>
    </Row>
  );
};

export default Profile;
