import React from 'react';



function Search() {
  return (
    <>
      <div className="content">
        <div className="terminal-pointer"></div>
        {/* <span className="material-symbols-outlined">navigate_next</span> */}
        <input type="text" className="form-field" id="search-bar" placeholder="Enter name"/>
      </div>
  </>
  );
}

export default Search;
