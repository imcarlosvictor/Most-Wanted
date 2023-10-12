import DatabasePage from './pages/DatabasePage';
import AnalyticsPage from './pages/AnalyticsPage';
import ChoroplethPage from './pages/ChoroplethPage';
import AboutPage from './pages/AboutPage';
import Home from './pages/HomePage';
import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from 'react-router-dom';
// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'


// function App() {
//   const [count, setCount] = useState(0)
//   return (
//     <>
//       <div className="content">

//         <nav className="navbar">
//           <span className="material-symbols-outlined">info</span>
//           <div className="nav-button-div">
//             <ul className="buttons">
//               <li><a href="#">Database</a></li>
//               <li><a href="#">Analytics</a></li>
//               <li><a href="#">Choropleth</a></li>
//               <li><a href="#">About</a></li>
//             </ul>
//           </div>
//         </nav>

//         <div className="terminal-pointer"></div>
//         {/* <span className="material-symbols-outlined">navigate_next</span> */}
//         <input type="text" className="form-field" id="search-bar" placeholder="Name, Location, Year"/>

//       </div>
//   </>
//   )
// }

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route path="/" element={<Home />}/>
      <Route path="/about" element={<AboutPage />}/>
      <Route path="/database" element={<DatabasePage />}/>
      <Route path="/analytics" element={<AnalyticsPage />}/>
      <Route path="/choropleth" element={<ChoroplethPage />}/>
    </Route>
  )
);

const App = () => {
  return <RouterProvider router={router} />;
}

export default App
