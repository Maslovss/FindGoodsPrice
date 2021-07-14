import React, { Component, useMemo, useState, useEffect } from "react";

import axios from "axios";

import Table from "./Table";
import SearchBar from "./SearchBar.js";

class App extends Component {
  constructor() {
    super();
    this.state = {
      server_hostname: "localhost",
      query: "",
      data: [],
      searchString: [],
    };

    this.columns = [
      {
        // Second group - Details
        Header: "Details",
        // Second group columns
        columns: [
          {
            Header: "Topic1",
            accessor: "topic1",
          },
          {
            Header: "Topic2",
            accessor: "topic2",
          },
          {
            Header: "Topic3",
            accessor: "topic3",
          },
          {
            Header: "Name",
            accessor: "name",
          },
          {
            Header: "Price",
            accessor: "price",
          },
          {
            Header: "Sale",
            accessor: "price_discount",
          },
        ],
      },
    ];
  }

  handleInputChange = (event) => {
    this.setState(
      {
        query: event.target.value,
      },
      () => {
        this.getData();
      }
    );
  };

  getData = () => {
    var url = "http://" + this.state.server_hostname + ":8080";
    if (this.state.query != "") {
      url = "http://" + this.state.server_hostname + ":8080/find/" + this.state.query;
    }

    fetch(url)
      .then((response) => response.json())
      .then((responseData) => {
        // console.log(responseData)
        this.setState({
          data: responseData,
          searchString: responseData,
        });
      });
  };

  filterArray = () => {
    var searchString = this.state.query;
    var responseData = this.state.data;
    if (searchString.length > 0) {
      // console.log(responseData[i].name);
      responseData = responseData.filter((l) => {
        console.log(l.name.toLowerCase().match(searchString));
      });
    }
  };

  componentWillMount() {
    this.getData();
  }

  render() {
    return (
      <div className="App">
        <div>
          <form>
            <input
              type="text"
              id="filter"
              placeholder="Search for..."
              ref={(input) => (this.search = input)}
              onChange={this.handleInputChange}
            />
          </form>
        </div>
        <Table columns={this.columns} data={this.state.data} />
      </div>
    );
  }
}

export default App;
