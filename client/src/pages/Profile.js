import React, { useEffect } from "react";
import { Col, Row } from "react-bootstrap";
import ProfileSidebar from "../components/Profile/ProfileSidebar"
import { Routes, Route } from "react-router-dom";
import Orders from "../components/Profile/Orders";
import Comments from "../components/Profile/comment/Comments";
import Address from "../components/Profile/address/Address";
import { useDispatch } from "react-redux";
import { getLocations } from "../features/stateCity/stateCitySlice";

const Profile = () => {
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(getLocations())
  }, [dispatch])
  
  return (
    <Row>
      <Col md={4}>
        <ProfileSidebar />
      </Col>
      <Col md={8}>
        <Routes>
          <Route path="/orders" element={<Orders />} />
          <Route path="/comments" element={<Comments />} />
          <Route path="/address" element={<Address />} />
        </Routes>
      </Col>
    </Row>
  );
};

export default Profile;
