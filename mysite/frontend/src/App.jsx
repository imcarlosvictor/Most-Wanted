import React from 'react';
import render from 'react-dom';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/NavBar';
import Search from './components/Search'
import About from './components/About'
import Database from './components/Database'
import Analytics from './components/Analytics'
import Map from './components/Map'
import './App.css';


function App(props) {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" elements={<Search/>}/>
        <Route path="/about" elements={<About/>}/>
        <Route path="/database" elements={<Database/>}/>
        <Route path="/analytics" elements={<Analytics/>}/>
        <Route path="/map" elements={<Map/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
