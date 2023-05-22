import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import Test from './Test';

const GOOGLE_MAPS_API_KEY = 'AIzaSyB4k2WLIJibVJ8ZmDTHtalCRVcDbfkPepM';

function loadScript(src, position, id) {
  if (!position) {
      return;
  }

  const script = document.createElement('script');
  script.setAttribute('async', '');
  script.setAttribute('id', id);
  script.src = src;
  position.appendChild(script);
}

const root = ReactDOM.createRoot(document.getElementById('root'));
if (typeof window !== 'undefined') {
  if (!document.querySelector('#google-maps')) {
      loadScript(
          `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}&libraries=places`,
          document.querySelector('head'),
          'google-maps',
      );
  }
}
root.render(
  <React.StrictMode>
    <Test/>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
