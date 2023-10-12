import React from 'react';



export default function Home() {
  return (
    <>
      <div className="content">
        <nav className="navbar">
          <span className="material-symbols-outlined">info</span>
          <div className="nav-button-div">
            <ul className="buttons">
              <li><a href="#">Database</a></li>
              <li><a href="#">Analytics</a></li>
              <li><a href="#">Choropleth</a></li>
              <li><a href="#">About</a></li>
            </ul>
          </div>
        </nav>
        <div className="terminal-pointer"></div>
        {/* <span className="material-symbols-outlined">navigate_next</span> */}
        <input type="text" className="form-field" id="search-bar" placeholder="Name, Location, Year"/>
      </div>
  </>
  )
}
