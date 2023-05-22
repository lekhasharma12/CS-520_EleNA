import { Component } from "react";

class Location extends Component {
    constructor(props) {
        super(props);

        const {lat, lng} = this.props.initialCenter;

        this.state = {
            currentLocation: {
                lat: lat,
                lng: lng
            }
        }
    }
}