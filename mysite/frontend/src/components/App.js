import React, { Component } from "react";
import { render } from "react-dom";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return <h1>Testing React Code</h1>;
  }
}

const appDiv = document.getElementsByClassName("content");
render(<App />, appDiv);
