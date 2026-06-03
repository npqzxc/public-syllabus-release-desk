export function createStore(initialState) {
  let state = initialState;
  return {
    getState() {
      return state;
    },
    setState(next) {
      state = { ...state, ...next };
    },
  };
}
