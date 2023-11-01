import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import profiles from '../api/profiles';


export default function Search() {
  const [profileInfo, setProfileInfo] = useState([]);

  const fetchProfiles = async () => {
    try {
      const response = await profiles.get('/profiles/')
      setProfileInfo(response.data)
      // console.log(response)
    } catch (error) {
      console.log(error);
    }
  }

  const createSearchBar = () => {

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

  useEffect( () => {
    var input = document.getElementById("search-bar");
    input.addEventListener("keyup", function(event) {
      if (event.keyCode == 13) {
        filterTable(event);
      }
    });
  });

  function filterTable(event) {
    let search_bar = document.getElementById("search-bar");
    let user_input = search_bar.value.toLowerCase();
    let flag = false;
    console.log(`User input:${user_input}`);
    
    // Search for profile
    for (let i = 0; i < profileInfo.length; i++) {
      if (profileInfo[i]["name"].trim() === user_input.trim()) {
        console.log("###############");
        console.log(`FOUND: ${profileInfo[i]["name"]}`);
        console.log("###############");
        return;
      }
    }
  }

  useEffect( () => {
    fetchProfiles();
  }, [])

  return (
    <>
      {createSearchBar()};
    </>
  );
}
