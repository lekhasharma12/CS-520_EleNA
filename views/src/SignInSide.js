import React, { Component } from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
// import MyComponents from './Map';
import { Autocomplete, Slider } from '@mui/material';
import axios from 'axios';
// import AutoComplete from './AutoComplete';
// import Auto from './AutoComplete';
import GoogleMaps from './AutoComplete';

// import { Loader } from "@googlemaps/js-api-loader"

const defaultTheme = createTheme();

class SignInSide extends Component {

    constructor(props) {
        super(props);

        this.state = {
            sourceSuggestions: [],
            source: '',
            destination: '',
            elevation: 0,
            mode: 0,
            percent: 0,
        }

        // const loader = new Loader({
        //     apiKey: "AIzaSyB4k2WLIJibVJ8ZmDTHtalCRVcDbfkPepM",
        //     version: "weekly",
        //     // ...additionalOptions,
        // });

        // loader.load().then(async (google) => {
        //     const { Map } = await google.maps.importLibrary("maps");

        //     let map = new Map(document.getElementById("map"), {
        //         center: { lat: -34.397, lng: 150.644 },
        //         zoom: 8,
        //     });
        //     console.log("🚀 ~ file: SignInSide.js:55 ~ SignInSide ~ map=newMap ~ map:", map)
            
        // });

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

    }

    handleChange(event) {
        // console.log("🚀 ~ file: Form.js:17 ~ Form ~ handleChange ~ event:", event)
        const target = event.target
        const name = target.name

        const value = target.value

        // axios.defaults.baseURL = 'http://localhost:5000';

        // axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
        // axios.defaults.headers.common['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept';

        // return <Auto/>

        // const proxyUrl = 'https://cors-anywhere.herokuapp.com/';

        // var config = {
        //     method: 'get',
        //     url: `http://localhost:5000/elena/autocomplete`,
        //     headers: { 
        //         'Content-Type': 'application/json',
        //         "Access-Control-Allow-Origin": "*",
        //         "Access-Control-Allow-Methods": "GET,PUT,POST,DELETE,PATCH,OPTIONS"
        //     },
        //     withCredentials: false
        // };

        // axios.get( proxyUrl+config.url)
        //     .then(function (response) {
        //         console.log(JSON.stringify(response.data));
        //     })
        //     .catch(function (error) {
        //         console.log("error-------------", error);
        //     });

        // var requestOptions = {
        //     method: 'GET',
        //     redirect: 'follow'
        //   };
          
        //   fetch(`http://127.0.0.1:5000/elena/autocomplete?search=puff&location=12`, requestOptions)
        //     .then(response => response.json())
        //     .then((result) => {
        //         console.log("🚀 ~ file: SignInSide.js:98 ~ SignInSide ~ .then ~ result:", result)
        //         this.setState({sourceSuggestions: result.predictions})
        //     })
        //     .catch(error => console.log('error', error));



        // this.setState({ [name]: target.value });
    }

    handleSubmit(event) {
        console.log("🚀 ~ file: SignInSide.js:60 ~ SignInSide ~ handleSubmit ~ event:", event)

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
                        {/* <Grid
                        sx={{
                            my: 4,
                            mx: 0,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            backgroundColor: 'green'
                        }}
                        > */}
                        {/* <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                            <LockOutlinedIcon />
                        </Avatar> */}
                        <Grid
                            sx={{
                                ml: 10,
                                mt: 10
                                // backgroundColor:'green'
                            }}
                        >
                            <Typography component="h1" variant="h5" align='center'>
                                EleNa
                            </Typography>
                            <Grid
                                component="form"
                                onSubmit={this.handleSubmit}
                                sx={{
                                    mt: 1,
                                    mr: 10,
                                    display: 'flex',
                                    flexDirection: 'column',
                                    // backgroundColor: 'blue'
                                }}
                                fullWidth
                            // style={{}}

                            >
                                <Grid
                                    sx={{
                                        display: 'flex',
                                        flexDirection: 'row',
                                        // backgroundColor: 'black'
                                    }}
                                >
                                    {/* <Button
                                component="img"
                                // src='source.png'
                                // style={{marginTop: 25, marginRight: 5}}
                            /> */}
                                    <img
                                        src={require('./source.png')}
                                        style={{
                                            width: 15, height: 15,
                                            marginTop: 30, marginRight: 8
                                        }}
                                    />
                                   
                                    {/* <TextField
                                        // style={{width: '300px'}}
                                        margin="normal"
                                        // required
                                        fullWidth
                                        id="source"
                                        label="Source"
                                        name="source"
                                        // autoComplete="email"
                                        autoFocus
                                        size='small'
                                        onChange={this.handleChange}
                                    /> */}
                                    <GoogleMaps/>

                                </Grid>
                                <Grid
                                    sx={{
                                        display: 'flex',
                                        flexDirection: 'row',
                                        // backgroundColor: 'black'
                                    }}
                                >
                                    <img
                                        src={require('./destination.png')}
                                        style={{
                                            width: 20, height: 20,
                                            marginTop: 25, marginRight: 5
                                        }}
                                    />
                                    <TextField
                                        margin="normal"
                                        size='small'
                                        // required
                                        fullWidth
                                        name="destination"
                                        label="Destination"
                                        // type="password"
                                        id="destination"
                                    // autoComplete="current-password"
                                    />
                                </Grid>
                                {/* <FormControlLabel
                                    control={<Checkbox value="remember" color="primary" />}
                                    label="Remember me"
                             /> */}
                                <Grid sx={{
                                    // backgroundColor:'red',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    // backgroundColor:'black',
                                    mt: 5
                                }}>
                                    <Typography
                                        component="h5"
                                    // style={{backgroundColor:'red'}}
                                    // sx = {{
                                    //     mt:3,
                                    // }}
                                    >
                                        Elevation and Mode
                                    </Typography>
                                    <Grid sx={{
                                        // mt: -2,
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
                                                style={{
                                                    // width: 15, height: 15,
                                                    // marginTop: 30, marginRight: 8,
                                                    tintColor: 'blue',

                                                }}
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
                                            // style={{
                                            //     // width: 15, height: 15,
                                            //     // marginTop: 30, marginRight: 8,
                                            //     // tintColor: 'blue'
                                            // }}
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
                                            console.log("value", event.target.value)
                                            this.setState({ percent: event.target.value })
                                        }}
                                    />
                                    <Typography
                                        sx={{
                                            ml: 25
                                            // backgroundColor: 'black'
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
                                    >
                                        Find Path
                                    </Button>
                                    {/* </Grid> */}
                                </Grid>

                                <Grid container>
                                    {/* <Grid item xs>
                    <Link href="#" variant="body2">
                        Forgot password?
                    </Link>
                    </Grid> */}
                                    {/* <Grid item>
                    <Link href="#" variant="body2">
                        {"Don't have an account? Sign Up"}
                    </Link>
                    </Grid> */}
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                    {/* <MyComponents /> */}
                </Grid>
            </ThemeProvider>
        );
    }
}

export default SignInSide;