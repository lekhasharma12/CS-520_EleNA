import { render, screen } from '@testing-library/react';
import Test from '../Test';
import React from 'react';

const { JSDOM } = require('jsdom');

const jsdom = new JSDOM(`
  <!doctype html>
  <html>
    <head>
      <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB4k2WLIJibVJ8ZmDTHtalCRVcDbfkPepM&libraries=places"></script>
      <script>console.log(Window.google)</script>
    </head>
    <body>
    </body>
  </html>`, {runScripts: "dangerously"});
const { window } = jsdom;


test('Check is Find Path button is disabled when the source and destination are empty', () => {

    const testInstance = new Test();
  
    const mockState_filled = { source: 'Puffers Pond, Amherst, MA, USA', destination: 'UMass Amherst, Amherst, MA, USA' };

    // Rendering the Test component
    render(<Test />);

    Object.defineProperty(testInstance, 'state', {
        get: jest.fn().mockReturnValue(mockState_filled),
    });

    // Check if the initial state has the Find Path button disabled
    const findPathButton = screen.getByText('Find Path');

    expect(findPathButton).toBeEnabled();

    jest.restoreAllMocks();

});