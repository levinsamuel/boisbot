
import React, {Component} from 'react';
import Header from './Header';
import Footer from './Footer';
import Search from './Search';

import {Switch, Route, Redirect} from 'react-router-dom';

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

export default Main;
