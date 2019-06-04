import React from 'react';
import { BrowserRouter as Router, Route, NavLink } from 'react-router-dom';
import {BattlescribeSchemaTree} from './BattlescribeSchemaTree';
import './App.css';

class Navbar extends React.Component {
    render() {
        return (
            <nav className="navbar navbar-expand-lg navbar-light" style={{backgroundColor: "#C55F21"}}>
                <a className="navbar-brand" href="#" style={{color: "#2F3035"}}>Roster</a>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav mr-auto">
                        <li className="nav-item">
                            <NavLink exact className="nav-link" to="/">Home</NavLink>
                        </li>
                        <li className="nav-item">
                            <NavLink exact className="nav-link" to="/battlescribe/schema">Battlescribe Schema</NavLink>
                        </li>
                    </ul>
                </div>
            </nav>
        )
    }
}

export {Navbar};