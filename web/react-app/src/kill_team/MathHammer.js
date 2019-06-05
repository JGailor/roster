import React from 'react';
import {Container, Row, Col, Form} from "react-bootstrap";

class KillTeamMathHammer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            attacker: {
                hits: "",
                bs_ws: "",
                s: "",
                ap: "",
                d: "",
                ah: false,
            },
            defender: {
                t: "",
                sv: "",
                inv_sv: "",
                w: "",
                fw: ""
            },
            unobstructed: {
                hits: null,
                wounds: null,
                saves: null,
                death: null
            },
            obstructed: {
                hits: null,
                wounds: null,
                saves: null,
                death: null
            },
            obstructed_wc: {
                hits: null,
                wounds: null,
                saves: null,
                death: null
            } 
        }

        // Includes a 0 to make lookups simpler
        this.d6_odds_of_at_least_table = [1.0, 1.0, 0.83, 0.66, 0.50, 0.33, 0.17, 0.0];
        this.onAttackerChange = this.onAttackerChange.bind(this);
        this.onDefenderChange = this.onDefenderChange.bind(this);
    }

    checkAllFields() {
        let field;
        for (field in this.state.attacker) {
            if (field !== "ah") {
                if (!Number.isInteger(this.state.attacker[field])) {
                    return false;
                }
            }
        }

        for (field in this.state.defender) {
            if (field !== "inv_sv" && field !== "fw") {
                if (!Number.isInteger(this.state.defender[field])) {
                    return false;
                }
            }
        }

        return true;
    }

    woundTable(s, t) {
        if (s >= 2 * t) {
            return this.d6_odds_of_at_least_table[2];
        } else if (s > t) {
            return this.d6_odds_of_at_least_table[3];
        } else if (s == t) {
            return this.d6_odds_of_at_least_table[4];
        } else {
            return this.d6_odds_of_at_least_table[5];
        }
    }

    calculateD6Odds(num_die, gt) {
        let odds_of_not_rolling = 1.0;
        for (let i = 0; i < num_die; i++) {
            odds_of_not_rolling = odds_of_not_rolling * (1.0 - this.d6_odds_of_at_least_table[gt]);
        }
        return 1.0 - odds_of_not_rolling;
    }

    calculateAttackOdds(attacker, defender, hit_modifier, injury_modifier) {
        const invulnerable_save = Number.isInteger(defender.inv_sv) ? defender.inv_sv : 9999;
        let hits_connect; 
        if (attacker.ah) {
            hits_connect = attacker.hits;
        } else {
            hits_connect = this.d6_odds_of_at_least_table[attacker.bs_ws + hit_modifier];
        }

        const wounds = hits_connect * this.woundTable(attacker.s, defender.t);
        const modified_sv = defender.sv + Math.abs(attacker.ap) > 6 ? 7 : defender.sv + Math.abs(attacker.ap);
        const min_save = Math.min(...[modified_sv, invulnerable_save]);
        const passed_save = wounds - (wounds * this.d6_odds_of_at_least_table[min_save]);
        let chance_of_death = 0.0;
        const fw = Number.isInteger(defender.fw) ? defender.fw : 0;

        chance_of_death = this.calculateD6Odds(attacker.d, (4 + injury_modifier - fw));

        return {hits: hits_connect.toPrecision(2), wounds: wounds.toPrecision(2), saves: passed_save.toPrecision(2), death: chance_of_death.toPrecision(2)};
    }

    calculateUnobstructed(attacker, defender) {
        return this.calculateAttackOdds(attacker, defender, 0, 0);
    }

    calculateObstructed(attacker, defender) {
        return this.calculateAttackOdds(attacker, defender, 1, 0);
    }

    calculateObstructedWithCover(attacker, defender) {
        return this.calculateAttackOdds(attacker, defender, 1, 1);
    }

    calculateChanceToKill() {
        if (!this.checkAllFields()) {
            return;
        }

        const attacker = this.state.attacker;
        const defender = this.state.defender;

        const unobstructed  = this.calculateUnobstructed(attacker, defender);
        const obstructed    = this.calculateObstructed(attacker, defender);
        const obstructed_wc = this.calculateObstructedWithCover(attacker, defender);

        console.log(unobstructed);

        this.setState({
            ...this.state,
            unobstructed: unobstructed,
            obstructed: obstructed,
            obstructed_wc: obstructed_wc
        });
    }

    onAttackerChange(e) {
        console.log(e.target.value);

        const name = e.target.name;
        let parsed_value;

        if (name === "ah") {
            parsed_value = e.target.checked;
        } else {
            let value = parseInt(e.target.value);
            parsed_value = Number.isInteger(value) ? value : "";
        }

        console.log(parsed_value);
        this.setState({
            attacker: {
                ...this.state.attacker,
                [name]: parsed_value
            }
        }, () => this.calculateChanceToKill());
    }

    onDefenderChange(e) {
        const name = e.target.name;
        const value = parseInt(e.target.value);
        const parsed_value = Number.isInteger(value) ? value : "";;

        this.setState({
            defender: {
                ...this.state.defender,
                [name]: parsed_value 
            }
        }, () => this.calculateChanceToKill());
    }

    render() {
        return (
            <Container>
                <Form>
                    <Row>
                        <Col lg="5"><h2 style={{textAlign: "center"}}>Attacker</h2></Col>
                        <Col lg={{span: 5, offset: 2}}><h2 style={{textAlign: "center"}}>Defender</h2></Col>
                    </Row>
                    <Row>
                        <Col lg="1"><p className="text-center">Auto-Hit</p></Col>
                        <Col lg="1"><p className="text-center">Hits</p></Col>
                        <Col lg="1"><p className="text-center">BS/WS</p></Col>
                        <Col lg="1"><p className="text-center">S</p></Col>
                        <Col lg="1"><p className="text-center">AP</p></Col>
                        <Col lg="1"><p className="text-center">D</p></Col>
                        <Col lg="1"></Col>
                        <Col lg="1"><p className="text-center">T</p></Col>
                        <Col lg="1"><p className="text-center">Sv</p></Col>
                        <Col lg="1"><p className="text-center">Inv. Sv</p></Col>                        
                        <Col lg="1"><p className="text-center">W</p></Col> 
                        <Col lg="1"><p className="text-center">Flesh W.</p></Col>
                    </Row>
                    <Row>
                        <Col lg="1"><Form.Check type="checkbox" name="ah" onChange={this.onAttackerChange} checked={this.state.attacker.ah}/></Col>
                        <Col lg="1"><Form.Control type="input" name="hits" className="text-center" onChange={this.onAttackerChange} value={this.state.attacker.hits}></Form.Control></Col>
                        <Col lg="1"><Form.Control type="input" name="bs_ws" className="text-center" onChange={this.onAttackerChange} value={this.state.attacker.bs_ws}></Form.Control></Col>
                        <Col lg="1"><Form.Control type="input" name="s" className="text-center" onChange={this.onAttackerChange} value={this.state.attacker.s}></Form.Control></Col>
                        <Col lg="1"><Form.Control type="input" name="ap" className="text-center" onChange={this.onAttackerChange} value={this.state.attacker.ap}></Form.Control></Col>
                        <Col lg="1"><Form.Control type="input" name="d" className="text-center" onChange={this.onAttackerChange} value={this.state.attacker.d}></Form.Control></Col>
                        <Col lg="1"></Col>
                        <Col lg="1"><Form.Control type="input" name="t" className="text-center" onChange={this.onDefenderChange} value={this.state.defender.t}></Form.Control></Col>
                        <Col lg="1"><Form.Control type="input" name="sv" className="text-center" onChange={this.onDefenderChange} value={this.state.defender.sv}></Form.Control></Col>
                        <Col lg="1"><Form.Control type="input" name="inv_sv" className="text-center" onChange={this.onDefenderChange} value={this.state.defender.inv_sv}></Form.Control></Col>
                        <Col lg="1"><Form.Control type="input" name="w" className="text-center" onChange={this.onDefenderChange} value={this.state.defender.w} /></Col>
                        <Col lg="1"><Form.Control type="input" name="fw" className="text-center" onChange={this.onDefenderChange} value={this.state.defender.fw} /></Col>
                    </Row>
                </Form>
                <Row><Col><p></p></Col></Row>
                <Row>
                    <Col lg="3"></Col>
                    <Col lg="1"></Col>
                    <Col lg="1">Hits Succeed</Col>
                    <Col lg="1">Wounds Succeed</Col>
                    <Col lg="1">Chance to Injure</Col>
                    <Col lg="1">Chance to Kill</Col>
                </Row>
                <Row>
                    <Col lg="3"><p style={{textAlign: "right"}}>Unobstructed: </p></Col>
                    <Col lg="1"></Col>
                    <Col lg="1"><p>{this.state.unobstructed.hits}</p></Col>
                    <Col lg="1"><p>{this.state.unobstructed.wounds}</p></Col>
                    <Col lg="1"><p>{this.state.unobstructed.saves}</p></Col>
                    <Col lg="1"><p>{this.state.unobstructed.death}</p></Col>
                </Row>
                <Row>
                    <Col lg="3"><p style={{textAlign: "right"}}>Obstructed Without Cover: </p></Col>
                    <Col lg="1"></Col>
                    <Col lg="1"><p>{this.state.obstructed.hits}</p></Col>
                    <Col lg="1"><p>{this.state.obstructed.wounds}</p></Col>
                    <Col lg="1"><p>{this.state.obstructed.saves}</p></Col>
                    <Col lg="1"><p>{this.state.obstructed.death}</p></Col>
                </Row>
                <Row>
                    <Col lg="3"><p style={{textAlign: "right"}}>Obstructed: With Cover</p></Col>
                    <Col lg="1"></Col>
                    <Col lg="1"><p>{this.state.obstructed_wc.hits}</p></Col>
                    <Col lg="1"><p>{this.state.obstructed_wc.wounds}</p></Col>
                    <Col lg="1"><p>{this.state.obstructed_wc.saves}</p></Col>
                    <Col lg="1"><p>{this.state.obstructed_wc.death}</p></Col>
                </Row>
            </Container>
        );
    }
}

export {KillTeamMathHammer};