import React, { Component } from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { Slider } from '@mui/material';
import GoogleMaps from './AutoComplete';
import MyComponents from './Map';
import { BarLoader } from 'react-spinners';
import {DirectionsWalk, DirectionsBike, Brightness1Outlined, LocationOn} from '@mui/icons-material';

const defaultTheme = createTheme();

class Test extends Component {

    constructor(props) {
        super(props);

        this.state = {
            sourceSuggestions: [],
            source: '',
            destination: '',
            elevation: 0,
            mode: 0,
            percent: 0,
            results: '',
            path: [],
            loading: false,
        }
        this.handleSubmit = this.handleSubmit.bind(this);

    }

    handleDataFromChild(data, id) {
        this.setState({ [id]: data })
    }

    async handleSubmit(event) {


        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        let mode, elevation

        if (this.state.mode == 0) {
            mode = 'bike'
        } else {
            mode = 'walk'
        }

        if (this.state.elevation == 0) {
            elevation = 'min'
        } else {
            elevation = 'max'
        }

        if (this.state.source == '' || this.state.destination == '') {
            alert('Please input source and destination!!')
            return
        }

        var raw = JSON.stringify({
            "source": this.state.source,
            "destination": this.state.destination,
            "mode": mode,
            "elevation_type": elevation,
            "percent_increase": this.state.percent.toString()
        });

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        this.setState({ loading: true })


        fetch("http://127.0.0.1:5000/elena/shortestpath", requestOptions)
            .then(response => response.json())
            .then(result => {
                this.setState({ results: result })

                const convertedCoordinates = result.path.map(([lng, lat]) => ({
                    lat: lat,
                    lng: lng
                }));
                this.setState({ path: convertedCoordinates })
                this.setState({ loading: false })

            })
            .catch(error => {
                console.log('error', error)
                alert(`Some Error ocurred! Please try again later`)
                this.setState({ loading: false })
            });
    }

    render() {
        return (
            <ThemeProvider theme={defaultTheme}>
                <Grid container component="main" sx={{ height: '1vh', display: 'flex'}}>
                    <CssBaseline />
                    <Grid
                        // md={5}
                        component={Paper}
                        sx={{
                            // width: '100px',
                            justifyContent: 'center', alignItems: 'center'
                        }}
                        item xs={5}
                    >
                        <Grid
                            sx={{
                                ml: 10
                            }}
                        >
                            <img
                                src={require('./assets/logo.png')}
                                style={{
                                    width: 135, height: 75, alignSelf: 'center', marginLeft: "28%"
                                }}
                            />
                            <Grid
                                component="form"
                                sx={{
                                    mt: -2,
                                    mr: 10,
                                    display: 'flex',
                                    flexDirection: 'column'
                                }}
                                fullWidth
                            >
                                <Grid
                                    sx={{
                                        display: 'flex',
                                        flexDirection: 'row',
                                    }}
                                >
                                    <Grid item xs={1}>
                                        <Brightness1Outlined sx={{ color: '#1976d2', width:18, height:18, marginTop: '25px', marginLeft: '2px'}}/>
                                    </Grid>
                                    <Grid item xs={11}>
                                        <GoogleMaps
                                        id="source"
                                        label="Source"
                                        name="source"
                                        onData={(data, id) => this.handleDataFromChild(data, id)}
                                    />
                                    </Grid>
                                </Grid>
                                <Grid
                                    sx={{
                                        display: 'flex',
                                        flexDirection: 'row',
                                    }}
                                >
                                    <Grid item xs={1} justify="flex-end" alignItems="center">
                                        <LocationOn sx={{ color: '#1976d2', width:25, height:35, marginTop: '20px', marginRight: '-2px'}}/>
                                    </Grid>
                                    <Grid item xs={11}>
                                        <GoogleMaps
                                        id="destination"
                                        label="Destination"
                                        name="destination"
                                        onData={(data, id) => this.handleDataFromChild(data, id)}
                                    />
                                    </Grid>

                                </Grid>
                                <Grid sx={{
                                    display: 'flex',
                                    flexDirection: 'column',
                                    mt: 5
                                }}>
                                    <Typography
                                        component="h5"
                                        sx={{ fontWeight: 'bold' }}
                                    >
                                        Elevation and Mode
                                    </Typography>
                                    <Grid sx={{
                                        mt: 1, mb: 2,
                                        display: 'flex',
                                        flexDirection: 'row'
                                    }}>
                                        <Button
                                            type="button"
                                            fullWidth
                                            variant={this.state.elevation === 0 ? 'contained' : 'outlined'}
                                            sx={{ borderRadius: 0, height: 40 }}
                                            size='small'
                                            onClick={() => {
                                                this.setState({ elevation: 0 })
                                            }}
                                        >
                                            Min
                                        </Button>
                                        <Button
                                            type="button"
                                            fullWidth
                                            variant={this.state.elevation === 1 ? 'contained' : 'outlined'}
                                            sx={{ borderRadius: 0, height: 40 }}
                                            size='small'
                                            onClick={() => {
                                                this.setState({ elevation: 1 })
                                            }}
                                        >
                                            Max
                                        </Button>
                                    </Grid>
                                    <Grid sx={{
                                        mt: -4,
                                        display: 'flex',
                                        flexDirection: 'row'
                                    }}>
                                        <Button
                                            type="button"
                                            fullWidth
                                            variant={this.state.mode === 0 ? 'contained' : 'outlined'}
                                            sx={{ mt: 3, mb: 2, borderRadius: 0, height: 40 }}
                                            size='small'
                                            onClick={() => {
                                                this.setState({ mode: 0 })
                                            }}
                                        >
                                            <DirectionsBike/>
                                        </Button>
                                        <Button
                                            type="button"
                                            fullWidth
                                            variant={this.state.mode === 1 ? 'contained' : 'outlined'}
                                            sx={{ mt: 3, mb: 2, borderRadius: 0, height: 40}}
                                            size='small'
                                            onClick={() => {
                                                this.setState({ mode: 1 })
                                            }}
                                        >
                                            <DirectionsWalk/>
                                        </Button>
                                    </Grid>
                                    <Typography
                                        component="h5"
                                        sx={{
                                            mt: 3,
                                            fontWeight: 'bold'
                                        }}
                                    >
                                        % increase from shortest path
                                    </Typography>
                                    <Slider
                                        value={this.state.percent}
                                        size="small"
                                        defaultValue={70}
                                        aria-label="Small"
                                        valueLabelDisplay="auto"
                                        onChange={(event) => {
                                            this.setState({ percent: event.target.value })
                                        }}
                                    />
                                    <Typography
                                        sx={{
                                            ml: 25
                                        }}
                                    >
                                        {this.state.percent}%
                                    </Typography>
                                    <Button
                                        type="button"
                                        fullWidth
                                        variant="contained"
                                        size='large'
                                        sx={{ mt: 5, mb: 2, borderRadius: 0, height: 40}}
                                        onClick={async (event) => {
                                            await this.handleSubmit(event)
                                        }}
                                    >
                                        Find Path
                                    </Button>
                                </Grid>
                                <Grid>
                                    {this.state.loading === true ?
                                        <Grid sx={{ ml: 20 }}>
                                            <BarLoader color="#1976d2" />
                                        </Grid>
                                        :
                                        this.state.results != '' &&
                                        <Grid height={100}>
                                            <Typography sx={{ marginLeft: 10, fontSize: 20 }}>
                                                Estimated Time: {(this.state.results.time).toFixed(2)} hour(s)
                                            </Typography>
                                            <Typography sx={{ marginLeft: 10, fontSize: 20 }}>
                                                Total Distance: {(this.state.results.distance).toFixed(2)} km
                                            </Typography>
                                            <Typography sx={{ marginLeft: 10, fontSize: 20 }}>
                                                Elevation Variance : {this.state.results.elevation[1] -this.state.results.elevation[0]} m
                                            </Typography>
                                        </Grid>
                                    }

                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item xs={7}>
                        <MyComponents
                        path={this.state.path}
                    />
                    </Grid>
                </Grid>
                <Grid>

                </Grid>
            </ThemeProvider >
        );
    }
}

export default Test;