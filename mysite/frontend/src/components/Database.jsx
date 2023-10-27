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
          <p id="profile-entry-header-details">ID</p>
          <p id="profile-entry-header-details">name</p>
          <p id="profile-entry-header-details">alias</p>
          <p id="profile-entry-header-details">sex</p>
          <p id="profile-entry-header-details">charges</p>
          <p id="profile-entry-header-details">status</p>
          <p id="profile-entry-header-details">wanted by</p>
        </div>
        <table className="compiled-profile-database">
          {profileInfo.map(profile => {
            let sex_classname = "profile-entry-details";
            profile.sex == "male" ? sex_classname += " male" : sex_classname += " female";

            let charges_classname = "profile-entry-details";
            profile.charges == "male" ? charges_classname += " male" : charges_classname += " female";

            let wanted_by_classname = "profile-entry-details";
            profile.wanted_by == "male" ? wanted_by_classname += " male" : wanted_by_classname += " female";

            return (
              <tr className="profile-entry" key={profile.id}>
                <td className="profile-entry-details">{profile.id}</td>
                <td className="profile-entry-details">{profile.name}</td>
                <td className="profile-entry-details">{profile.alias}</td>
                <td className={sex_classname}>{profile.sex}</td>
                <td className="profile-entry-details">{profile.charges}</td>
                <td className="profile-entry-details"><span className="status-value">{profile.status}</span></td>
                <td className="profile-entry-details">{profile.wanted_by}</td>
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
