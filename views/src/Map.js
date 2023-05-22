import React, { Component } from 'react';
import { GoogleMap, Polyline } from '@react-google-maps/api';

const containerStyle = {
    width: '800px',
    height: '800px'
};

const center = {
    lat: 0,
    lng: -180
};

const options = {
    strokeColor: '#24A0ED',
    strokeOpacity: 10,
    strokeWeight: 6,
    fillColor: '#24A0ED',
    fillOpacity: 0.35,
    clickable: false,
    draggable: false,
    editable: false,
    visible: true,
    radius: 30000,
    zIndex: 1
};

const onLoad = polyline => {
    console.log('polyline: ', polyline)
};

class MyComponents extends Component {
    constructor(props) {
        super(props);

        this.state = {
            currentLocation: center,
            options: options,
            path: [],
            center: ''
        }
    }

    componentDidMount() {

        if (navigator && navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(pos => {

                const coords = pos.coords;
                this.setState({
                    currentLocation: {
                        lat: coords.latitude,
                        lng: coords.longitude
                    }
                });
            });
        }
    }

    componentDidUpdate(prevProps) {
        if (prevProps.path !== this.props.path) {
            this.setState({ path: this.props.path });
            let latSum = 0, lngSum = 0
            for (let i = 0; i < this.props.path.length; i++) {
                const item = this.props.path[i]
                latSum += item.lat
                lngSum += item.lng
            }
            const center = {
                lat: latSum / this.props.path.length,
                lng: lngSum / this.props.path.length
            }
            this.setState({ currentLocation: center })
        }
    }

    render() {

        return (
            <div>
                {this.state.path.length == 0 ?
                    <GoogleMap
                        mapContainerStyle={containerStyle}
                        center={this.state.currentLocation}
                        zoom={14}
                    >
                    </GoogleMap>
                    :
                    <GoogleMap
                        mapContainerStyle={containerStyle}
                        center={this.state.currentLocation}
                        zoom={14}
                    >
                        <Polyline
                            onLoad={onLoad}
                            path={this.state.path}
                            options={options}
                        />
                    </GoogleMap>
                }
            </div>
        )
    }
}

export default MyComponents