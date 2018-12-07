import * as Actions from './actions';

export const SearchReducer = (state = {
  icon: null,
  loading: false,
  err: null
}, action) => {
  switch (action.type) {
    case Actions.LOADING_USER:
      return {...state, loading: true, icon: null};
    case Actions.SHOW_USER:
      return {...state, icon: action.payload, loading: false};
    case Actions.USER_NOT_FOUND:
      return {...state, err: action.payload, loading: false};
    default:
      return state;
  }
};
