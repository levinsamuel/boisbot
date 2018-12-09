
import {createStore, combineReducers, applyMiddleware} from 'redux';
import thunk from 'redux-thunk';
import logger from 'redux-logger';
import {createForms} from 'react-redux-form';
import {SearchReducer} from './reducer';

const initialSearchState = {
  user: ''
};

export const ConfigureStore = () => {
  const store = createStore(
    combineReducers({
      search: SearchReducer,
      ...createForms({
        searchForm: initialSearchState
      })
    }),
    applyMiddleware(thunk, logger)
  );

  return store;
}
