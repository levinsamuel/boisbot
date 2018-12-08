import {actions} from 'react-redux-form';
import * as Actions from './actions';
import BASEURL from '../shared/baseUrl';

export const fetchIcon = user => dispatch => {

  dispatch(load(user));
  return fetch(BASEURL + 'user/' + user + '/icon', {
        credentials: 'same-origin'
      })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          console.error('Response not ok:', response)
          throw new Error(response.statusText);
        }
      })
      .then(response => dispatch(showUser(response.url)))
      .then(() => dispatch(actions.reset('searchForm')))
      .catch(error => dispatch(userNotFound(error)));
}

const load = user => ({
  type: Actions.LOADING_USER,
  payload: user
})

const showUser = iconUrl => ({
  type: Actions.SHOW_USER,
  payload: iconUrl
})

const userNotFound = error => {
  console.error('error:', error);
  return {
    type: Actions.USER_NOT_FOUND,
    payload: {
      error,
      code: 404
    }
  }
}
