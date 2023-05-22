import React, { Component } from 'react';

class Form extends Component {

    constructor(props) {
        super(props);
        this.state = {
            // value: ''
            source: '',
            destination: '',
            elevation: '',
            mode: '',
            percent: ''
        };

        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        console.log("🚀 ~ file: Form.js:17 ~ Form ~ handleChange ~ event:", event)
        const target = event.target
        const name = target.name

        this.setState({ [name]: target.value });
    }

    render() {
        return (
            <form>
                <div style={{display: 'flex', flexDirection: 'column', gap: '12px'}}>
                    <label style={{display: 'flex', flexDirection: 'row', gap: '10px'}}>
                        <img src='./logo192.png' />
                        {/* <br /> */}
                        <input
                            type="text"
                            name='source'
                            value={this.state.source}
                            onChange={this.handleChange}
                            placeholder='Source'
                            style={{width:'150px'}}
                        />
                    </label>
                    <label style={{display: 'flex', flexDirection: 'row', gap: '10px'}}>
                        {/* <br /> */}
                        <img src='./logo192.png' />
                        <input
                            type="text"
                            name='destination'
                            value={this.state.destination}
                            onChange={this.handleChange}
                            placeholder='Destination'
                            style={{width:'150px'}}
                        />
                    </label>
                </div>
                <div>
                    <p>
                        Elevation and Mode
                    </p>
                </div>
                <div style={{display: 'flex', flexDirection: 'row'}}>
                    
                    <button>
                        Min
                    </button>
                    <button>
                        Max
                    </button>
                </div>
            </form>
        )
    }
}

export default Form;