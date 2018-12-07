
import {createStore, combineReducers, applyMiddleware} from 'redux';
import thunk from 'redux-thunk';
import logger from 'redux-logger';
import {createForms} from 'react-redux-form';
import {Reducer, initialState} from './reducer';

const initialSearchState = {
  user: ''
};

export const ConfigureStore = () => {
  const store = createStore(
    combineReducers({
      main: Reducer,
      ...createForms({
        search: initialSearchState
      })
    }),
    applyMiddleware(thunk, logger)
  );

  return store;
}
