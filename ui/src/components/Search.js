import React, {Component} from 'react';
import {Breadcrumb, BreadcrumbItem, Button, Label,
  Input, Col, Row} from 'reactstrap';
import {Link} from 'react-router-dom';
import {Control, Form} from 'react-redux-form';
import {BounceLoader} from 'react-spinners';

class Search extends Component {

  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  render() {

    return (
      <div className="container">
        <div className="row row-content">
          <div className="col-12">
            <h3>Search for a user</h3>
          </div>
          <div className="col-12">
            <Form model="searchForm" onSubmit={this.handleSubmit}>
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
                  <Button disabled={this.props.loading}>Search
                  </Button>
                </Col>
              </Row>
            </Form>
          </div>
        </div>
        <div className="row row-content">
          <div className="col-12">
            <BounceLoader size={60} color="#1e90ff"
                loading={this.props.loading}/>
          </div>
          <div className="col-sm-6">
            <Icon imgurl={this.props.iconUrl}/>
          </div>
        </div>
      </div>
    );
  }

  handleSubmit(values) {
    console.debug('values', values);
    this.props.fetchIcon(values.user);
  }
}

const Icon = (props) => {

  if (props.imgurl) {
    return (
      <div className="icon">
        <img className="icon-img" src={props.imgurl}/>
      </div>
    )
  } else {
    return (<div></div>)
  }
}

export default Search;
