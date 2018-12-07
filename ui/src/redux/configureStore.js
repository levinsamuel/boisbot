
import {createStore, applyMiddleware} from 'redux';
import {Reducer, initialState} from './reducer';
import thunk from 'redux-thunk';
import logger from 'redux-logger';

export const ConfigureStore = () => {
  const store = createStore(
    Reducer,
    initialState,
    applyMiddleware(thunk, logger)
  );

  return store;
}
