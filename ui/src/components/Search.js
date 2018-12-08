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
        <div className="row row-content align-items-center justify-content-center">
          <Icon imgurl={this.props.iconUrl} user={this.props.user}
              loading={this.props.loading}/>
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
      <>
        <div className="col-12 col-sm-5">
          <div className="icon">
            <img className="icon-img" src={props.imgurl}/>
          </div>
        </div>
        <div className="col-12 col-sm-5">
          <div className="handle">
            <a href={`https://twitter.com/${props.user}`} target="_blank">
              <h4>{'@' + props.user}</h4>
            </a>
          </div>
        </div>
      </>
    )
  } else if (props.loading) {
    return (
      <div className="col-12 col-sm-5">
        <BounceLoader size={60} color="#1e90ff"
            loading={props.loading}
            className="justify-content-center"/>
      </div>
    )
  } else {
    return (<div></div>)
  }
}

export default Search;
