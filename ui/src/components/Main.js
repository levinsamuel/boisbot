
import React, {Component} from 'react';
import {withRouter} from 'react-router-dom';
import {connect} from 'react-redux';
import Header from './Header';
import Footer from './Footer';
import Search from './Search';
import {fetchIcon} from '../redux/creators';

const mapStateToProps = state => ({
  search: state.search
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
        <Search
            fetchIcon={this.props.fetchIcon}
            loading={this.props.search.loading}
            user={this.props.search.user}
            iconUrl={this.props.search.icon}
          />
        <Footer/>
      </div>
    );
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Main));
