import React from 'react'
import {Col,Row} from 'react-bootstrap';
import ProfileSidebar from '../components/ProfileSidebar';
import { Routes, Route } from "react-router-dom";
import Orders from "../components/Profile/Orders";
import Comments from "../components/Profile/Comments";




const Profile = () => {
    // const [window,setWindow] = useState(false)

  return (
    <Row>
        <Col md={4}>
            <ProfileSidebar/>
        </Col>
        <Col md={8}>
            <Routes>
                <Route path="/orders" element={<Orders />} />
                <Route path="/comments" element={<Comments />} />
                
            </Routes>
        </Col>
    </Row>

  )
}

export default Profile