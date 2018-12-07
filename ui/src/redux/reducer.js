import * as Actions from './actions';

export const SearchReducer = (state = {
  icon: null,
  loading: false
}, action) => {
  switch (action.type) {
    case Actions.LOADING_USER:
      return {...state, loading: true};
    case Actions.SHOW_USER:
      return {...state, icon: action.payload, loading: false};
    default:
      return state;
  }
};
