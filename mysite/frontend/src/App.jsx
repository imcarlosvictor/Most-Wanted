import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import render from 'react-dom';
import Navbar from './components/NavBar';
import Search from './components/Search';
import About from './components/About';
import Database from './components/Database';
import Analytics from './components/Analytics';
import Map from './components/Map';
import './App.css';


export default function App() {
  const createRouter = () => {
    return (
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Search/>}/>
          <Route path="/about" element={<About/>}/>
          <Route path="/database" element={<Database/>}/>
          <Route path="/analytics" element={<Analytics/>}/>
          {/* <Route path="/map" element={<Map/>}/> */}
        </Routes>
      </BrowserRouter>
    )
  }
  return (
    <>
      {createRouter()}
    </>
  )
}
