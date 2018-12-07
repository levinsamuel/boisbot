import {actions} from 'react-redux-form';
import * as Actions from './actions';
import BASEURL from '../shared/baseUrl';

export const fetchIcon = user => dispatch => {

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
      .then(response => console.log("Response:", response))
      .then(() => actions.reset('search'))
      .catch(error => {
        console.error("failed request: ", error.message)
      });
}
