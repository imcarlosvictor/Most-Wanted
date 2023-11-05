import { React, useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import profiles from '../api/profiles';



export default function ProfileDetails() {
  const params = useParams();

  const [profileInfo, setProfileInfo] = useState([]);
  const fetchProfiles = async () => {
    try {
      const response = await profiles.get('/profiles/')
      setProfileInfo(response.data)
    } catch (error) {
      console.log(error);
    }
  }

  // TODO: Redirect to 404 if profile id does not exist

  // Allows data to persist once the user refreshes the page
  // Grab data
  useEffect(() => {
    const data = window.localStorage.getItem("profile-target")
    if (data !== null) {
      setProfileInfo(JSON.parse(data))
    }
  }, [])
  // Store data
  useEffect(() => {
    window.localStorage.setItem("profile-target", JSON.stringify(profileInfo));
  }, [profileInfo])
  
  let profileTargetData = {}

  // Find profile in profileInfo
  for (let i = 0; i < profileInfo.length; i++) {
    if (profileInfo[i]["id"] == params["profileID"]) {
      console.log(profileInfo[i])
      profileTargetData["id"] = profileInfo[i]["id"]
      profileTargetData["name"] = profileInfo[i]["name"]
      profileTargetData["alias"] = profileInfo[i]["alias"]
      profileTargetData["sex"] = profileInfo[i]["sex"]
      profileTargetData["height_in_cm"] = profileInfo[i]["height_in_cm"]
      profileTargetData["weight_in_kg"] = profileInfo[i]["weight_in_kg"]
      profileTargetData["eyes"] = profileInfo[i]["eyes"]
      profileTargetData["hair"] = profileInfo[i]["hair"]
      profileTargetData["distinguishing_marks"] = profileInfo[i]["distinguishing_marks"]
      profileTargetData["nationality"] = profileInfo[i]["nationality"]
      profileTargetData["date_of_birth"] = profileInfo[i]["date_of_birth"]
      profileTargetData["place_of_birth"] = profileInfo[i]["place_of_birth"]
      profileTargetData["charges"] = profileInfo[i]["charges"]
      profileTargetData["wanted_by"] = profileInfo[i]["wanted_by"]
      profileTargetData["status"] = profileInfo[i]["status"]
      profileTargetData["publication"] = profileInfo[i]["publication"]
      profileTargetData["last_modified"] = profileInfo[i]["last_modified"]
      profileTargetData["reward"] = profileInfo[i]["reward"]
      profileTargetData["details"] = profileInfo[i]["details"]
      profileTargetData["caution"] = profileInfo[i]["caution"]
      profileTargetData["remarks"] = profileInfo[i]["remarks"]
      profileTargetData["images"] = profileInfo[i]["images"]
      profileTargetData["link"] = profileInfo[i]["link"]
      break;
    }
  }

  // Add n/a values if no data exists
  for (let [key, value] of Object.entries(profileTargetData)) {
    console.log(key, value);
    if (value == "") {
      profileTargetData[key] = 'n/a';
    }
  }

  console.log(profileTargetData["name"])
  const createProfileDisplay = () => {
    return (
      <>
        <div className="noise-bg"></div>
        <div className="profile-target-body">

          <div className="profile-target-content">
            <div className="profile-image">
              <p className="profile-data" id="image">{profileTargetData["image"]}</p>
            </div>

            <div className="target-details content-id">
              <div className="detail-content">
                <p className="label" id="id-label">id</p>
                <p className="profile-data" id="id">{profileTargetData["id"]}</p>
              </div>

              <div className="detail-content content-status">
                <p className="label" id="status-label">status</p>
                <p className="profile-data" id="status">{profileTargetData["status"]}</p>
              </div>

              <div className="detail-content content-wanted-by">
                <p className="label" id="wanted-by-label">wanted by</p>
                <p className="profile-data" id="wanted_by">{profileTargetData["wanted_by"]}</p>
              </div>

              <div className="detail-content content-charges">
                <p className="label" id="charges-label">charges</p>
                <p className="profile-data" id="charges">{profileTargetData["charges"]}</p>
              </div>

              <div className="modification-status">
                <div className="detail-content content-publication">
                  <p className="label" id="publication-label">publication</p>
                  <p className="profile-data" id="publication">{profileTargetData["publication"]}</p>
                </div>

                <div className="detail-content content-last-modified">
                  <p className="label" id="last-modified-label">last modified</p>
                  <p className="profile-data" id="last_modified">{profileTargetData["last_modified"]}</p>
                </div>
              </div>
            </div>


            <div className="intro-details">
              <div className="detail-content">
                <p className="label" id="name-label">name</p>
                <p className="profile-data" id="name">{profileTargetData["name"]}</p>
              </div>
              <div className="detail-content">
                <p className="label" id="alias-label">alias</p>
                <p className="profile-data" id="alias">{profileTargetData["alias"]}</p>
              </div>
              <div className="detail-content">
                <p className="label" id="place-of-birth-label">place of birth</p>
                <p className="profile-data" id="place_of_birth">{profileTargetData["place_of_birth"]}</p>
              </div>
              <div className="detail-content">
                <p className="label" id="date-of-birth-label">date of birth</p>
                <p className="profile-data" id="date_of_birth">{profileTargetData["date_of_birth"]}</p>
              </div>
              <div className="detail-content">
                <p className="label" id="nationality-label">nationality</p>
                <p className="profile-data" id="nationality">{profileTargetData["nationality"]}</p>
              </div>
            </div>

            <div className="physical-details">
              <div className="detail-content">
                <p className="label" id="sex-label">sex</p>
                <p className="profile-data" id="sex">{profileTargetData["sex"]}</p>
              </div>
              <div className="detail-content">
                <p className="label" id="marks-label">marks</p>
                <p className="profile-data" id="distinguishing_marks">{profileTargetData["distinguishing_marks"]}</p>
              </div>
              <div className="detail-content">
                <p className="label" id="height-label">height</p>
                <p className="profile-data" id="height_in_cm">{profileTargetData["height_in_cm"]} cm</p>
              </div>
              <div className="detail-content">
                <p className="label" id="weight-label">weight</p>
                <p className="profile-data" id="weight_in_kg">{profileTargetData["weight_in_kg"]} kg</p>
              </div>
              <div className="detail-content">
                <p className="label" id="eyes-label">eyes</p>
                <p className="profile-data" id="eyes">{profileTargetData["eyes"]}</p>
              </div>
              <div className="detail-content">
                <p className="label" id="hair-label">hair</p>
                <p className="profile-data" id="hair">{profileTargetData["hair"]}</p>
              </div>
            </div>

            <div className="target-summary">
              <div className="detail-content content-details">
                <p className="label" id="details-label">details</p>
                <p className="profile-data" id="details">{profileTargetData["details"]}</p>
              </div>

              <div className="detail-content">
                <p className="label" id="remarks-label">remarks</p>
                <p className="profile-data" id="remarks">{profileTargetData["remarks"]}</p>
              </div>
            </div>

          </div>
        </div>

      </>
    )
  }

  useEffect( () => {
    fetchProfiles();
  }, [])

  return (
    <>
      {createProfileDisplay()}
    </>
  );
}
