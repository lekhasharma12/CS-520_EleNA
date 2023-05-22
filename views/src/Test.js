import React, { Component } from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { AlertTitle, Slider } from '@mui/material';
import GoogleMaps from './AutoComplete';
import MyComponents from './Map';
import Spinner from 'react-bootstrap/Spinner';
import {BarLoader}  from 'react-spinners';

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
            isError: false
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleError = this.handleError.bind(this);

    }

    handleDataFromChild(data, id) {
        this.setState({ [id]: data })
    }

    handleError() {
        this.setState({isError: false})
        alert("Please enter all inputs!")
        
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

        if(this.state.source == '' || this.state.destination == '') {
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

        this.setState({loading: true})

        
        fetch("http://127.0.0.1:5000/elena/shortestpath", requestOptions)
            .then(response => response.json())
            .then(result => {
                this.setState({ results: result })
                
                const convertedCoordinates = result.path.map(([lng, lat]) => ({
                    lat: lat,
                    lng: lng
                }));
                this.setState({ path: convertedCoordinates })
                this.setState({loading: false})
                
            })
            .catch(error => {
                console.log('error', error)
                alert(`Some Error ocurred! Please try again later`)
                this.setState({loading: false})
            });
    }

    render() {
        return (
            <ThemeProvider theme={defaultTheme}>
                <Grid container component="main" sx={{ height: '1vh' }}>
                    <CssBaseline />
                    
                    {/* <Auto/> */}
                    <Grid
                        // fullWidth
                        md={5}
                        component={Paper}
                        sx={{
                            width: '100px',
                        }}
                    >
                        <Grid
                            sx={{
                                ml: 10,
                                // mt: 4
                            }}
                        >
                            <img
                                src={require('./assets/elena_logo.png')}
                                style={{
                                    width: 100, height: 100,
                                    marginLeft: 170, backgroundColor:'red'
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
                                    <img
                                        src={require('./assets/source.png')}
                                        style={{
                                            width: 15, height: 15,
                                            marginTop: 30, marginRight: 8
                                        }}
                                    />
                                    <GoogleMaps
                                        id="source"
                                        label="Source"
                                        name="source"
                                        onData={(data, id) => this.handleDataFromChild(data, id)}
                                    />
                                </Grid>
                                <Grid
                                    sx={{
                                        display: 'flex',
                                        flexDirection: 'row',
                                    }}
                                >
                                    <img
                                        src={require('./assets/destination.png')}
                                        style={{
                                            width: 20, height: 20,
                                            marginTop: 25, marginRight: 5
                                        }}
                                    />
                                    <GoogleMaps
                                        id="destination"
                                        label="Destination"
                                        name="destination"
                                        onData={(data, id) => this.handleDataFromChild(data, id)}
                                    />
                                </Grid>
                                <Grid sx={{
                                    display: 'flex',
                                    flexDirection: 'column',
                                    mt: 5
                                }}>
                                    <Typography
                                        component="h5"
                                        sx={{fontWeight:'bold'}}
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
                                            sx={{ borderRadius: 0, height: 50 }}
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
                                            sx={{ borderRadius: 0 }}
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
                                            sx={{ mt: 3, mb: 2, borderRadius: 0 }}
                                            size='small'
                                            onClick={() => {
                                                this.setState({ mode: 0 })
                                            }}
                                        >
                                            <img
                                                src={require('./assets/ion_bicycle.png')}
                                            />
                                        </Button>
                                        <Button
                                            type="button"
                                            fullWidth
                                            variant={this.state.mode === 1 ? 'contained' : 'outlined'}
                                            sx={{ mt: 3, mb: 2, borderRadius: 0 }}
                                            size='small'
                                            onClick={() => {
                                                this.setState({ mode: 1 })
                                            }}
                                        >
                                            <img
                                                src={require('./assets/walk.png')}
                                            />
                                        </Button>
                                    </Grid>
                                    <Typography
                                        component="h5"
                                        sx={{
                                            mt: 3,
                                            fontWeight:'bold'
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
                                        sx={{ mt: 5, mb: 2, borderRadius: 0, height: 60 }}
                                        onClick={async (event) => {
                                            await this.handleSubmit(event)
                                        }}
                                    >
                                        Find Path
                                    </Button>
                                </Grid>
                                <Grid>
                                    {this.state.loading === true ? 
                                        <Grid sx={{ml: 20}}>
                                            <BarLoader color="#24a0ed"/>
                                        </Grid>
                                        :
                                        this.state.results != '' &&
                                        <Grid height={100}>
                                            {/* <Typography sx={{ marginLeft: 10, fontSize: 20 }}>
                                                Estimated Time: {this.state.results.time}
                                            </Typography> */}
                                            <Typography sx={{ marginLeft: 10, fontSize: 20 }}>
                                                Total Distance: {this.state.results.distance}
                                            </Typography>
                                            <Typography sx={{ marginLeft: 10, fontSize: 20 }}>
                                                Minimum Elevation Gain: {this.state.results.elevation[0]}
                                            </Typography>
                                            <Typography sx={{ marginLeft: 10, fontSize: 20 }}>
                                                Maximum Elevation Gain: {this.state.results.elevation[1]}
                                            </Typography>
                                        </Grid>
                                    }
                                    
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                    <MyComponents
                        path={this.state.path}
                    />
                </Grid>
                <Grid>

                </Grid>
            </ThemeProvider >
        );
    }
}

export default Test;



// {this.state.results != '' ?
//                                         <Grid height={100}>
//                                             <Typography sx={{ marginLeft: 10, fontSize: 20 }}>
//                                                 Estimated Time: {this.state.results.time}
//                                             </Typography>
//                                             <Typography sx={{ marginLeft: 10, fontSize: 20 }}>
//                                                 Total Distance: {this.state.results.distance}
//                                             </Typography>
//                                             <Typography sx={{ marginLeft: 10, fontSize: 20 }}>
//                                                 Elevation Gain: {this.state.results.elevation}
//                                             </Typography>
//                                         </Grid>
//                                         :
//                                         <Spinner animation="border"/>
//                                             // {/* <span className="visually-hidden">Loading...</span> */}
//                                         // </Spinner>
//                                     }