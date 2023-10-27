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
      <div className="database-content">
        <div id="profile-entry-header">
          <p id="profile-entry-header-details">name</p>
          <p id="profile-entry-header-details">sex</p>
          <p id="profile-entry-header-details">status</p>
          <p id="profile-entry-header-details">charges</p>
        </div>
        <table className="compiled-profile-database">
          {profileInfo.map(profile => {
            return (
              <tr className="profile-entry" key={profile.id}>
                <td className="profile-entry-details">{profile.name}</td>
                <td className="profile-entry-details">{profile.sex}</td>
                <td className="profile-entry-details"><span className="status-value">{profile.status}</span></td>
                <td className="profile-entry-details">{profile.charges}</td>
              </tr>
            )
          })}
        </table>
      </div>
    )
  }

  useEffect( () => {
    fetchProfiles();
  }, [])

  return (
    <>
      {createProfileCard()}
    </>
  );
}
