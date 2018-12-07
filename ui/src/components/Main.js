
import React, {Component} from 'react';
import {Switch, Route, Redirect, withRouter} from 'react-router-dom';
import {connect} from 'react-redux';
import Header from './Header';
import Footer from './Footer';
import Search from './Search';
import {fetchIcon} from '../redux/creators';

const mapStateToProps = state => ({
  main: state.main
});

const mapDispatchToProps = dispatch => ({
  fetchIcon: user => dispatch(fetchIcon(user))
})

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
