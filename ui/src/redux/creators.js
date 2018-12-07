import * as Actions from './actions';
import BASEURL from '../shared/baseUrl';

export const fetchIcon = user => dispatch => {

  return fetch(BASEURL + 'user/' + user + '/icon', {
        credentials: 'same-origin'
      })
      .then(response => {
        if (response.ok) {
          console.log("Response:", response);
        } else {
          throw new Error(response.message);
        }
      })
      .catch(error => {
        console.error("failed request: ", error.message)
      });
}
