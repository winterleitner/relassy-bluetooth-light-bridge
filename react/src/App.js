import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react'
import {Light} from "./components/Light";

//const BASEURL = "http://192.168.5.2:5000"
const BASEURL = ""

function App() {

  const [lights, setLights] = useState([])

  useEffect(async () => {
    const resp = await fetch(`${BASEURL}/scan`)
    const json = await resp.json()
    for (let i = 0; i < json.length; i++) {
        const l = json[i]
        const r = await fetch(`${BASEURL}/light?address=${encodeURI(l.address)}`)
        const text = await r.json()
        json[i].blue = text.blue
        json[i].white = text.white
    }
    setLights(json)
  }, [])
  return (
    <div className="App">
      <header className="App-header">
        <h2>
          Aquarium-Lampen steuern
        </h2>
        <ul>
          {lights.map(l => <Light name={l.name} address={l.address} blue={l.blue} white={l.white}/>)}
        </ul>
      </header>
    </div>
  );
}

export default App;
