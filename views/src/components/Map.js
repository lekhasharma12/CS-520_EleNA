import React, { Component } from 'react';
import { GoogleMap, Polyline, Marker} from '@react-google-maps/api';
import sourceMarker from './../assets/circle-fill.svg';

const containerStyle = {
    width: '840px',
    height: '800px'
};

const center = {
    lat: 0,
    lng: -180
};

const options = {
    strokeColor: '#1976d2',
    strokeOpacity: 1,
    strokeWeight: 3,
    // fillColor: '#1976d2',
    // fillOpacity: 0.35,
    // clickable: false,
    // draggable: false,
    // editable: false,
    // visible: true,
    // radius: 30000,
    // zIndex: 1
};

const onLoad = polyline => {
    console.log('polyline: ', polyline)
};

class Map extends Component {
    constructor(props) {
        super(props);

        this.state = {
            currentLocation: center,
            options: options,
            path: [],
            center: '',
            loading: false
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
            this.state.path = []
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
                        <Marker position={this.state.path[0]} icon={sourceMarker}></Marker>
                        <Marker position={this.state.path[this.state.path.length-1]}></Marker>
                        <Polyline
                            path={this.state.path}
                            options={options}
                        />
                    </GoogleMap>
                }
            </div>
        )
    }
}

export default Map