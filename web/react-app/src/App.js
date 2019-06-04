import React from 'react';
import { BrowserRouter as BrowserRouter, Route, Switch, Link } from 'react-router-dom';
import {BattlescribeSchemaTree} from './BattlescribeSchemaTree';
import {Navbar} from "./Navbar";
import './App.css';

function Index() {
  return (
    <div>
        <Navbar />
        <p>Welcome to Roster!</p>
        <p><Link to="/battlescribe/schema">Battlescribe Cat Schema Explorer</Link></p>
    </div>
  )
}

function BattlescribeCatSchemaExplorer() {
  return (
    <div>
      <Navbar/>
      <BattlescribeSchemaTree/>
    </div>)
}

class Roster extends React.Component {
  render() {
    return(
      <BrowserRouter>
        <Route exact path="/" component={Index}/>
        <Route exact path="/battlescribe/schema" component={BattlescribeCatSchemaExplorer}/>
      </BrowserRouter>
    );
  }
}

function App() {
  return (
    <Roster/>
  );
}

export default App;
