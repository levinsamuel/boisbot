
import React, {Component} from 'react';
import Header from './Header';
import Footer from './Footer';
import Search from './Search';
import {connect} from 'react-redux';

import {Switch, Route, Redirect, withRouter} from 'react-router-dom';

function mapStateToProps(state) {
  // return an object with same keys and values as state
  return {};
}

class Main extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="Main">
        <Header/>
        <Switch>
          <Route exact path="/" component={Search}/>
          <Redirect to="/"/>
        </Switch>
        <Footer/>
      </div>
    );
  }
}

export default withRouter(connect(mapStateToProps)(Main));
