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

  useEffect( () => {
    fetchProfiles();
  }, [])

  const createSearchBar = () => {
    return (
      <>
        <div className="content">
          <div className="terminal-pointer"></div>
          {/* <span className="material-symbols-outlined">navigate_next</span> */}
          <input type="text" className="form-field" id="search-bar" placeholder="Enter name"/>
        </div>
        <ul className="notifications"></ul>
      </>

    );
  }

  useEffect( () => {
    var input = document.getElementById("search-bar");
    var notifications = document.querySelector(".notifications");

    // Object containing details for different types of toasts
    const notifDetails = {
      timer: 5000,
      success: {
          icon: 'fa-circle-check',
          text: 'Success: This is a success toast.',
      },
      no_match: {
          icon: 'fa-circle-xmark',
          text: 'No Match: Name does not match any profiles',
      },
      warning: {
          icon: 'fa-triangle-exclamation',
          text: 'Warning: This is a warning toast.',
      },
    }

    // Remove notification after a set amount of time 
    const removeNotif = (notif) => {
      notif.classList.add("hide");
      if(notif.timeoutId) clearTimeout(notif.timeoutId); // Clearing the timeout for the toast
      setTimeout(() => notif.remove(), 500); // Removing the toast after 500ms
    }
  
    // Create notification card after user hit enter
    const createNotif = (result) => {
      // Getting the icon and text for the toast based on the id passed
      switch (result) {
        case "null":
          var result_value = "no_match";
          break;
      }

      const { icon, text } = notifDetails[result_value];
      const notif = document.createElement("li"); // Creating a new 'li' element for the toast
      notif.className = `notif ${result}`; // Setting the classes for the toast
      // Setting the inner HTML for the toast
      notif.innerHTML = `<div class="column">
                           <i class="fa-solid ${icon}"></i>
                           <span>${text}</span>
                        </div>
                        <i class="fa-solid fa-xmark" onclick="removeToast(this.parentElement)"></i>`;
      notifications.appendChild(notif); // Append the toast to the notification ul
      // Setting a timeout to remove the toast after the specified duration
      notif.timeoutId = setTimeout(() => removeNotif(notif), notifDetails.timer);
    }

    // Search bar event listener 
    input.addEventListener("keyup", function(event) {
      event.stopImmediatePropagation(); // Prevent event bubbling
      // event.stopPropagation();
      if (event.keyCode == 13) {
        // Check if user hit ENTER Key
        let profileID = filterTable();
        if (profileID == null) {
          createNotif("null");
        } else {
          console.log(`ID:${profileID}`);
        }
      }});
  });

  // Search for user input in the database of profiles
  function filterTable() {
    let search_bar = document.getElementById("search-bar");
    let user_input = search_bar.value.toLowerCase();
    let flag = false;
    // Search for profile
    for (let i = 0; i < profileInfo.length; i++) {
      if (profileInfo[i]["name"].trim() === user_input.trim()) {
        flag = true;
        return profileInfo[i]["id"];
      }
    }
    // No result
    if (!flag) {
      console.log(`No profile by the name ${user_input.toUpperCase()} found.`)
      return null;
    }
  }

  return (
    <>
      {createSearchBar()};
    </>
  );
}
