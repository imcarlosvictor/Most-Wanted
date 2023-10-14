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
          <div className="nav-button-list">
            <ul className="button-list">
              <li>
                <NavLink to="/">Search</NavLink>
              </li>
              <li>
                <NavLink to="/about">About</NavLink>
              </li>
              <li>
                <NavLink to="/database">Database</NavLink>
              </li>
              <li>
                <NavLink to="/analytics">Analytics</NavLink>
              </li>
              <li>
                <NavLink to="/map">Map</NavLink>
              </li>
            </ul>
          </div>
        </div>
    </nav>
  )
}

export default Navbar;
