import React from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCaretRight, faCaretDown} from '@fortawesome/free-solid-svg-icons';
import './App.css';

class TreeNode extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        collapsed: false
      }
    }
  
    handleTreeControlClick() {
      this.setState({collapsed: !this.state.collapsed});
    }
  
    attributes_list() {
      let attrs = [];
      for (let i = 0; i < this.props.attributes.length; i++) {
        attrs.push(<span key={i} className="attr" style={{color: "#0074D9", fontStyle: 'italic'}}>{this.props.attributes[i]}</span>);
        if (i < this.props.attributes.length - 1) {
          attrs.push(<span key={"attr_sep_" + i} className="attr-sep">, </span>);
        }
      }
  
  
      return attrs;
    }
  
    render() {
      const name = this.props.name;
      const styles = {marginLeft: this.props.indent * 10, paddingBottom: 5};
      let tree_control;
      let children;
  
      if (this.state.collapsed) {
        tree_control = <FontAwesomeIcon style={{width: 10}} icon={faCaretRight} onClick={() => this.handleTreeControlClick()}/>
      } else {
        tree_control = <FontAwesomeIcon style={{width: 10}} icon={faCaretDown} onClick={() => this.handleTreeControlClick()}/>
        children = this.props.children.map((data) => <TreeNode name={data.name} attributes={data.attributes.sort()} children={data.children} indent={this.props.indent + 1}/>);
      }
  
      return (
        <div>
          <div style={styles}>
            {tree_control}
            <span style={{marginLeft: 10, color: "#001f3f", fontWeight: "bold"}}>{name}</span>
            <span>({this.attributes_list()})</span>
          </div>
          {children}
        </div>
      );   
    }
}

class BattlescribeSchemaTree extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            schema: null,
            load_error: false
        }
    }

    handleLoadError(ex) {
        console.log("error loading data: ", ex);
        this.setState({load_error: true});
    }

    componentDidMount() {
        fetch("/api/battlescribe/w40k_8th/schema.json")
            .then((r) => r.json())
            .then(data => this.setState({schema: data}))
            .catch((ex) => this.handleLoadError(ex));
    }

    render() {
        let tree;

        if (this.state.schema) {
            tree = <TreeNode name={this.state.schema.name} attributes={this.state.schema.attributes.sort()} children={this.state.schema.children} indent={0}/>
        } else {
            if (this.state.load_error) {
                tree = <p>There was a problem loading the data... please try again</p>;
            } else {
                tree = <p>Loading...</p>;
            }
        }

        return (
            <div class="container">
                <h2 style={{marginTop: 15}}>Battlescribe .cat File Schema</h2>
                <hr/>
                {tree}
            </div>
        )
    }
}

export {BattlescribeSchemaTree};