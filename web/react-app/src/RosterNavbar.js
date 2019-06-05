import React from 'react';
import { NavLink } from 'react-router-dom';
import { Navbar, Nav, NavDropdown  } from "react-bootstrap";
import './App.css';

class RosterNavbar extends React.Component {
    render() {
        return (
            <Navbar style={{backgroundColor: "#C55F21"}}>
                <Navbar.Brand href="#" style={{color: "#2F3035"}}>Roster</Navbar.Brand>
                <Navbar.Collapse id="navbarSupportedContent">
                    <Nav className="mr-auto">
                        <NavLink exact className="nav-link" to="/">Home</NavLink>
                        <Nav.Item as="li">
                            <NavLink exact className="nav-link" to="/battlescribe/schema">Battlescribe Schema</NavLink>
                        </Nav.Item>
                        <NavDropdown title="Kill Team" as="li">
                            <ul>
                                <NavDropdown.Item as="li">
                                    <NavLink exact className="nav-link" to="/kt/mh">Math Hammer</NavLink>
                                </NavDropdown.Item>
                            </ul>
                        </NavDropdown>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        )
    }
}

export {RosterNavbar};