import React, { Component } from 'react';
import { GoogleMap, LoadScript } from '@react-google-maps/api';

const containerStyle = {
    width: '800px',
    height: '800px'
};

const center = {
    lat: -3.745,
    lng: -38.523
};

class MyComponents extends Component {
    constructor(props) {
        super(props);

        this.state = { currentLocation: center }
    }

    componentDidMount() {

        // console.log("lat ---------", this.state.currentLocation)

        if (navigator && navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(pos => {
                console.log("pos is --------->>>>>>>", pos)

                const coords = pos.coords;
                this.setState({
                    currentLocation: {
                        lat: coords.latitude,
                        lng: coords.longitude
                    }
                });

                console.log("lat ---------", this.state.currentLocation)
            });
        }
    }

    render() {

        return (

            <GoogleMap
                mapContainerStyle={containerStyle}
                center={this.state.currentLocation}
                zoom={10}
            />
        )
    }
}

export default MyComponents