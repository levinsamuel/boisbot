import React, {Component} from 'react';
import {Breadcrumb, BreadcrumbItem, Button, Label,
  Input, Col, Row} from 'reactstrap';
import {Link} from 'react-router-dom';
import {Control, Form} from 'react-redux-form';

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
            <Form model="search" onSubmit={this.handleSubmit}>
              <Row className="form-group">
                <Col>
                <Label htmlFor="usersearch">Twitter Username</Label>
                  <Control.text className="form-control" type="search"
                      name="user" id="user"
                      placeholder="Twitter User" model=".user"/>
                </Col>
              </Row>
              <Row className="form-group">
                <Col>
                  <Button>Search
                  </Button>
                </Col>
              </Row>
            </Form>
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
