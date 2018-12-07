
import React, {Component} from 'react';
import {Switch, Route, Redirect, withRouter} from 'react-router-dom';
import {connect} from 'react-redux';
import Header from './Header';
import Footer from './Footer';
import Search from './Search';
import {fetchIcon} from '../redux/creators';

function mapStateToProps(state) {
  // return an object with same keys and values as state
  return state;
}

function mapDispatchToProps(dispatch) {
  return {
    fetchIcon: user => dispatch(fetchIcon(user))
  }
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
          <Route exact path="/" component={
            () => <Search fetchIcon={this.props.fetchIcon}/>
          }/>
          <Redirect to="/"/>
        </Switch>
        <Footer/>
      </div>
    );
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Main));
