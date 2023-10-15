import { useState } from 'react';
import { NavLink, Link } from 'react-router-dom';



const Navbar = () => {
  const [showNavbar, setShowNavbar] = useState(false)

  // const handleShowNavbar = () => {
  //   setShowNavbar(!showNavbar)
  // }

  return (
    <nav className="navbar">
        <div className="navbar-container">
          <div className="navigation-list">
            <ul className="navigation-buttons">
              <li><span className="navlink-btn"><Link to="/" >Search</Link></span></li>
              <li><span className="navlink-btn"><Link to="/database">Database</Link></span></li>
              <li><span className="navlink-btn"><Link to="/analytics">Analytics</Link></span></li>
              <li><span className="navlink-btn"><Link to="/map">Map</Link></span></li>
              <li><span className="navlink-btn"><Link to="/about">About</Link></span></li>
            </ul>
          </div>
        </div>
    </nav>
  )
}

export default Navbar;

