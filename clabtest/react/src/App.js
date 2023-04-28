import React, { Component } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Home from './component/home';
import Contact from './component/contact';
import Drop from './component/drop';
import Register from './component/register';
import Login from './component/login';

import './App.css';

function Navbar() {
  const location = useLocation();
  const isDropOrRegisterRoute = location.pathname === '/drop' || location.pathname === '/register';

  return (
    <ul className="nav-list">
      <li><a href="/">Home</a></li>
      {!isDropOrRegisterRoute && <li><a href="#about">About</a></li>}
      {!isDropOrRegisterRoute && <li><a href="#contact">Contact</a></li>}
      <li><a href="register" id="register">Sign Up</a></li>
    </ul>
  );
}

class App extends Component {
  render() {
    return (
      <Router>
        <div className="navbar">
          <Navbar />
          <Routes>
            <Route exact path="/" element={<Home />}></Route>
            <Route exact path="/contact" element={<Contact />}></Route>
            <Route exact path="/drop" element={<Drop />}></Route>
            <Route exact path="/register" element={<Register />}></Route>
            <Route exact path="/login" element={<Login />}></Route>
          </Routes>
        </div>
      </Router>
    );
  }
}

export default App;
