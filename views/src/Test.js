import React, { Component } from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
// import MyComponents from './Map';
import { Slider } from '@mui/material';
import GoogleMaps from './AutoComplete';
import MyComponents from './Map';
import TextareaAutosize from '@mui/base/TextareaAutosize';

// import { Loader } from "@googlemaps/js-api-loader"

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
            results: ''
        }

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

    }

    handleChange(event) {
        const target = event.target
        const name = target.name

        const value = target.value

    }

    handleDataFromChild(data, id) {
        this.setState({[id]: data})
    }

    async handleSubmit(event) {

        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        let mode, elevation

        if (this.state.mode == 0) {
            mode = 'bike'
        } else{
            mode = 'walk'
        }

        if (this.state.elevation == 0) {
            elevation = 'min'
        } else{
            elevation = 'max'
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

        fetch("http://127.0.0.1:5000/elena/shortestpath", requestOptions)
            .then(response => response.json())
            .then(result => {
                this.setState({results: result})
            })
            .catch(error => console.log('error', error));
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
                            // backgroundColor: 'brown'

                        }}
                    >
                        <Grid
                            sx={{
                                ml: 10,
                                mt: 4
                                // backgroundColor:'green'
                            }}
                        >
                            <Typography component="h1" variant="h5" align='center'>
                                EleNa
                            </Typography>
                            <Grid
                                component="form"
                                // onSubmit={this.handleSubmit}
                                sx={{
                                    mt: 1,
                                    mr: 10,
                                    display: 'flex',
                                    flexDirection: 'column',
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
                                        src={require('./source.png')}
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
                                        src={require('./destination.png')}
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
                                                src={require('./ion_bicycle.png')}
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
                                                src={require('./walk.png')}
                                            />
                                        </Button>

                                    </Grid>

                                    <Typography
                                        component="h5"
                                        sx={{
                                            mt: 3
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
                                    {this.state.results != '' &&
                                        <Grid height={100}>
                                            <Typography sx={{ marginLeft: 10, fontSize: 20 }}>
                                                Estimated Time: {this.state.results.time}
                                            </Typography>
                                            <Typography sx={{ marginLeft: 10, fontSize: 20 }}>
                                                Total Distance: {this.state.results.distance}
                                            </Typography>
                                            <Typography sx={{ marginLeft: 10, fontSize: 20 }}>
                                                Elevation Gain: {this.state.results.elevation}
                                            </Typography>
                                        </Grid>
                                    }
                                    {/* :
                                    null
                                    } */}
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                    <MyComponents />
                </Grid>
                <Grid>

                </Grid>
            </ThemeProvider >
        );
    }
}

export default Test;