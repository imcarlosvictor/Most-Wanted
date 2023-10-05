import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (



    <div className="content">
      {/* <!-- <div class="terminal-pointer"></div> --> */}
      <span className="material-symbols-outlined">navigate_next</span>
      <input type="text" className="form-field" id="search-bar" placeholder="Name, Location, Year"/>
      <ul className="buttons">
        <li><a href="#">Database</a></li>
        <li><a href="#">Analytics</a></li>
        <li><a href="#">Choropleth</a></li>
        <li><a href="#">About</a></li>
      </ul>
    </div>






  )
}

export default App
