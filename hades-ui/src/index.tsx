import React from 'react';
import ReactDOM from 'react-dom/client';
import { Auth0Provider } from '@auth0/auth0-react';
import { Provider } from 'react-redux';


import './index.css';
import 'antd/dist/reset.css';
import reportWebVitals from './reportWebVitals';
import { RootRouter } from './routers';
import { store } from './store';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <Auth0Provider domain="dev-a2m7lmtzvdghj12e.us.auth0.com"
        clientId="WiXLFeytl0NwvTFOhISHcjOGBRuHZqmy"
        authorizationParams={{
          redirect_uri: window.location.origin,
          leeway: 1800
        }}>
        <RootRouter />
      </Auth0Provider>
    </Provider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
