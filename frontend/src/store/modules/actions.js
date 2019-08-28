import Axios from 'axios'
import state from 'state'

export default {
  logged_in (context, url) {
    Axios.post(state.base_url + '/api/loggedin', {
      token: context.state.token
    }).then(resp => {
      if (resp.data !== 'valid') {
        window.location.href = '/tryaccess/login/' + url;
      }
    }).catch(error => {
      console.log(error);
    })
  }
};