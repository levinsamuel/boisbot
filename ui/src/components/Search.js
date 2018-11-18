import React, {Component} from 'react';
import {Breadcrumb, BreadcrumbItem, Button, Form, FormGroup, Label, Input, Col} from 'reactstrap';
import {Link} from 'react-router-dom';

class Search extends Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (

        <div className="container">
          <div className="row">
            <h3>Search for a user</h3>
          </div>
          <div className="row row-content">
            <form>
              <div className="form-group">
                <label for="usersearch">Twitter Username</label>
                <input className="form-control" type="search" name="username" placeholder="Twitter User"/>

              </div>
            </form>
          </div>
        </div>
    );
  }
}

export default Search;
