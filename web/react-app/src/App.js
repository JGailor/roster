import React from 'react';
import { BrowserRouter, Route, Link } from 'react-router-dom';
import {BattlescribeSchemaTree} from './BattlescribeSchemaTree';
import {RosterNavbar} from "./RosterNavbar";
import {KillTeamMathHammer} from "./kill_team/MathHammer";
import './App.css';

function IndexView() {
  return (
    <div>
        <RosterNavbar />
        <p>Welcome to Roster!</p>
        <p><Link to="/battlescribe/schema">Battlescribe Cat Schema Explorer</Link></p>
    </div>
  )
}

function BattlescribeCatSchemaView() {
  return (
    <div>
      <RosterNavbar/>
      <BattlescribeSchemaTree/>
    </div>)
}

function KillTeamMathHammerView() {
  return (
    <div>
      <RosterNavbar/>
      <KillTeamMathHammer/>
    </div>
  )
}

class Roster extends React.Component {
  render() {
    return(
      <BrowserRouter>
        <Route exact path="/" component={IndexView}/>
        <Route exact path="/battlescribe/schema" component={BattlescribeCatSchemaView}/>
        <Route exact path="/kt/mh" component={KillTeamMathHammerView}/>
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
