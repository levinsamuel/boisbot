import React, {Component} from 'react';
import {Breadcrumb, BreadcrumbItem, Button, Form, FormGroup, Label,
  Input, Col} from 'reactstrap';
import {Link} from 'react-router-dom';
import {Control, LocalForm} from 'react-redux-form';

class Search extends Component {

  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  render() {

    return (
        <div className="container">
          <div className="row">
            <h3>Search for a user</h3>
          </div>
          <div className="row row-content">
            <LocalForm onSubmit={this.handleSubmit}>
              <div className="form-group">
                <Label htmlFor="usersearch">Twitter Username</Label>
                <Control.text className="form-control" type="search" name="username"
                    placeholder="Twitter User" model=".user"/>

              </div>
              <div className="form-group">
                <Button>Search
                </Button>
              </div>
            </LocalForm>
          </div>
        </div>
    );
  }

  handleSubmit(values) {
    console.debug('values', values);
    this.props.fetchIcon(values.user);
  }
}

export default Search;
