import React, { Component } from 'react';
import Main from './components/Main';
import {BrowserRouter, Switch, Route, Redirect} from 'react-router-dom';
import './styles/App.css';
import {Provider} from 'react-redux';
import {ConfigureStore} from './redux/configureStore'

const store = ConfigureStore();
class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <BrowserRouter>
          <div className="App">
            <Switch>
              <Route exact path="/" component={Main}/>
              <Redirect to="/"/>
            </Switch>
          </div>
        </BrowserRouter>
      </Provider>
    );
  }
}

export default App;
