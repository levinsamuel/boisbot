import {actions} from 'react-redux-form';
import * as Actions from './actions';
import BASEURL from '../shared/baseUrl';

export const fetchIcon = user => dispatch => {

  dispatch(load());
  return fetch(BASEURL + 'user/' + user + '/icon', {
        credentials: 'same-origin'
      })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error(response.message);
        }
      })
      .then(response => dispatch(showUser(response.url)))
      .then(() => dispatch(actions.reset('searchForm')))
      .catch(error => {
        console.error("failed request: ", error.message)
      });
}

const load = () => ({
  type: Actions.LOADING_USER
})

const showUser = iconUrl => ({
  type: Actions.SHOW_USER,
  payload: iconUrl
})
