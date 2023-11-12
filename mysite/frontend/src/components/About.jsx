import React from 'react';



export default function About() {
  return (
    <>
      <div className="noise-bg"></div>
      <div className="about-content">
        <p>The database is composed of active fugitive records that have been that have been compiled through various public sources.</p>
        <div className="source-list">
          <ul className="sources">
            <li className="source"><a href="https://www.fbi.gov/wanted/">FBI</a></li>
            <li className="source"><a href="https://www.interpol.int/en/How-we-work/Notices/Red-Notices/View-Red-Notices">Interpol</a></li>
            <li className="source"><a href="https://www.rcmp-grc.gc.ca/en/wanted">RCMP</a></li>
            {/* <li className="source"><a href="https://www.222tips.com/">Crime Stoppers Toronto</a></li> */}
            {/* <li className="source"><a href="https://www.tps.ca/organizational-chart/specialized-operations-command/detective-operations/investigative-services/homicide/most-wanted/">Toronto Police Service</a></li> */}
            {/* <li className="source"><a href="https://www.peelpolice.ca/Modules/News/Search.aspx?feedId=5dd101f7-e47a-4cdb-98c1-2e2cd6b2d1f9">Peel Regional Police</a></li> */}
          </ul>
        </div>
      </div>
    </>
  );
}
