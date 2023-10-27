import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import profiles from '../api/profiles'



export default function Database() {
  const [profileInfo, setProfileInfo] = useState([]);

  const fetchProfiles = async () => {
    try {
      const response = await profiles.get('/profiles/')
      setProfileInfo(response.data)
      console.log(response)
    } catch (error) {
      console.log(error);
    }
  }

  const createProfileCard = () => {
    return (
      <div className="compiled-profile-database">
        <div id="profile-entry-header">
          <p id="profile-entry-header-details">name</p>
          <p id="profile-entry-header-details">sex</p>
          <p id="profile-entry-header-details">status</p>
          <p id="profile-entry-header-details">charges</p>
        </div>
        {profileInfo.map(profile => {
          return (
            <div className="profile-entry" key={profile.id}>
              <p className="profile-entry-details">{profile.name}</p>
              <p className="profile-entry-details">{profile.sex}</p>
              <p className="profile-entry-details"><span className="status-value">{profile.status}</span></p>
              <p className="profile-entry-details">{profile.charges}</p>
            </div>
          )
        })}
      </div>
    )
  }

  useEffect( () => {
    fetchProfiles();
  }, [])

  return (
    <>
      <h2>Database</h2>
      {createProfileCard()}
    </>
  );
}
