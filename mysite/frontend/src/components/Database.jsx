import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import profiles from '../api/profiles';



export default function Database() {
  const [profileInfo, setProfileInfo] = useState([]);

  const fetchProfiles = async () => {
    try {
      const response = await profiles.get('/profiles/')
      setProfileInfo(response.data)
    } catch (error) {
      console.log(error);
    }
  }

  const createProfileTable = () => {
    return (
      <div className="database-content">
        <div id="profile-entry-header">
          <button id="id" className="table-column profile-entry-header-buttons" onClick={toggleArrow}>ID<i className="caret"></i></button>
          <button id="name" className="table-column profile-entry-header-buttons" onClick={toggleArrow}>name<i className="caret"></i></button>
          <button id="alias" className="table-column profile-entry-header-buttons">alias<i className="caret"></i></button>
          <button id="sex" className="table-column profile-entry-header-buttons" onClick={toggleArrow}>sex<i className="caret"></i></button>
          <button id="charges" className="table-column profile-entry-header-buttons">charges<i className="caret"></i></button>
          <button id="status" className="table-column profile-entry-header-buttons">status<i className="caret"></i></button>
          <button id="wanted_by" className="table-column profile-entry-header-buttons" onClick={toggleArrow}>wanted by<i className="caret"></i></button>
        </div>
        <table className="compiled-profile-database">
          <tbody id="table-body">
            {profileInfo.map(profile => {
              let sex_classname = "profile-entry-details";
              profile.sex == "male" ? sex_classname += " male" : sex_classname += " female";

              let wanted_by_classname = "profile-entry-details";
              if (profile.wanted_by) {
                wanted_by_classname += " " + profile.wanted_by;
              }

              let charges_classname = "profile-entry-details";
              const text = profile.charges.split(" ");
              for (let i = 0; i < text.length; i++) {
                switch(text[i].toLowerCase()) {
                  case "murder":
                    charges_classname += " murder";
                    break;
                  case "homicide":
                    charges_classname += " murder";
                    break;
                  case "rape":
                    charges_classname += " sex rape";
                    break;
                  case "abduction":
                    charges_classname += " abduction";
                    break;
                  case "terrorist":
                    charges_classname += " terrorist";
                    break;
                  case "parole":
                    charges_classname += " parole";
                    break;
                  case "driving":
                    charges_classname += " driving";
                    break;
                  case "road":
                    charges_classname += " driving";
                    break;
                  case "trafficking":
                    charges_classname += " trafficking";
                    break;
                  case "sexual":
                    charges_classname += " sex";
                    break;
                  case "drug":
                    charges_classname += " substance";
                    break;
                  case "narcotic":
                    charges_classname += " substance";
                    break;
                  case "substance":
                    charges_classname += " substance";
                    break;
                  case "fraud":
                    charges_classname += " fraud";
                    break;
                  case "femicide":
                    charges_classname += " femicide";
                    break;
                  case "child":
                    charges_classname += " child minor";
                    break;
                  case "minor":
                    charges_classname += " child minor";
                    break;
                  case "teenage":
                    charges_classname += " child minor";
                    break;
                  case "crime":
                    charges_classname += " crime";
                    break;
                  case "gang":
                    charges_classname += " crime";
                    break;
                  case "firearm":
                    charges_classname += " firearm ammunition";
                    break;
                  case "scam":
                    charges_classname += " scam";
                    break;
                  case "robbery":
                    charges_classname += " robbery";
                    break;
                  case "extortion":
                    charges_classname += " extortion";
                    break;
                  case "infanticide":
                    charges_classname += " murder infanticide";
                    break;
                  case "threats":
                    charges_classname += " threats";
                    break;
                }
              }

              return (
                <Link key={profile.id} to={"/details/" + profile.id} state={{ data:profileInfo }}>
                <tr className="profile-entry">
                  <td className="profile-entry-details">{profile.id}</td>
                  <td className="profile-entry-details">{profile.name}</td>
                  <td className="profile-entry-details">{profile.alias}</td>
                  <td className={sex_classname}>{profile.sex}</td>
                  <td className={charges_classname}>{profile.charges}</td>
                  <td className="profile-entry-details"><span className="status-value">{profile.status}</span></td>
                  <td className={wanted_by_classname}>{profile.wanted_by}</td>
                </tr>
                </Link>
              )
            })}
          </tbody>
        </table>
      </div>
    )
  }

  // filter
  // let input = document.getElementsByClassName("compiled-profile-database");
  var caretUpClassName = 'fa fa-caret-up';
  var caretDownClassName = 'fa fa-caret-down';


  const sortBy = (field, reverse, primer) => {
    const key = primer ?
      function(x) {
        return primer(x[field]);
      } :
      function(x) {
        return x[field];
      };
    reverse = !reverse ? 1 : -1;

    return function(a, b) {
      return a = key(a), b = key(b), reverse * ((a > b) - (b > a));
    };
  };

  function clearArrow() {
    let carets = document.getElementsByClassName('caret');
    for (let caret of carets) {
      caret.className = "caret";
    }
  }

  function toggleArrow(event) {
    event.stopPropagation();
    let element = event.target;
    let caret, field, reverse;
    if (element.tagName === 'BUTTON') {
      caret = element.getElementsByClassName('caret')[0];
      field = element.id;
    }
    else {
      caret = element;
      field = element.parentElement.id;
    }

    let iconClassName = caret.className;
    clearArrow();
    if (iconClassName.includes(caretUpClassName)) {
      caret.className = `caret ${caretDownClassName}`;
      reverse = false;
      console.log(reverse);
    } else {
      caret.className = `caret ${caretUpClassName}`;
      reverse = true;
      console.log(reverse);
    }

    // order list
    for ( let i = 0; i < profileInfo.length; i++ ) {
      profileInfo.sort(sortBy(field, reverse));
    }
    console.log(profileInfo);
    populateTable();
  }


  function populateTable() {
    let table = document.getElementById("table-body");
    table.innerHTML = '';

    // Fill rows with profile data
    for (let profileData of profileInfo) {
      let row = table.insertRow(-1);
      row.className = "profile-entry-details";
      let tableData = document.createElement("td")


      let pathname = "/details/" + profileData.id
      let link_parameters = `pathname:${pathname}, state:${profileData}`
      tableData.innerHTML = `
      <Link to={${link_parameters}}>
      <td className="id">${profileData.id}</td>
      <td className="name">${profileData.name}</td>
      <td className="alias">${profileData.alias}</td>
      <td className="sex">${profileData.sex}</td>
      <td className="charges">${profileData.charges}</td>
      <td className="status">${profileData.status}</td>
      <td className="wanted_by">${profileData.wanted_by}</td>
      </Link>
      `
      row.appendChild(tableData);

      // let table_row_btn = document.createElement("button");
      // table_row_btn.className = "profile-entry-btn"
      // table_row_btn.setAttribute("onclick", print);

      // let row = table.insertRow(-1);
      // row.className = "profile-entry-details";
      // row.addEventListener("event", print)

      // let id = row.insertCell(0);
      // id.innerHTML = profileData.id;
      // id.className = "id";

      // let name = row.insertCell(1);
      // name.innerHTML = profileData.name;
      // name.className = "name";

      // let alias = row.insertCell(2);
      // alias.innerHTML = profileData.alias;
      // alias.className = "alias";

      // let sex = row.insertCell(3);
      // sex.innerHTML = profileData.sex;
      // sex.className = "sex";

      // let charges = row.insertCell(4);
      // charges.innerHTML = profileData.charges;
      // charges.className = "charges";

      // let status = row.insertCell(5);
      // status.innerHTML = profileData.status;
      // status.className = "status";

      // let wanted_by = row.insertCell(6);
      // wanted_by.innerHTML = profileData.wanted_by;
      // wanted_by.className = "wanted_by";

    }
  }

  useEffect( () => {
    fetchProfiles();
  }, [])

  return (
    <>
      {createProfileTable()}
    </>
  );
}
