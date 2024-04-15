import React, { useState, useEffect } from "react";
import HighchartsReact from "highcharts-react-official";
import Highcharts from 'highcharts/highstock'
import axios from "axios";

import DarkUnica from 'highcharts/themes/dark-unica';

DarkUnica(Highcharts);

export const StockChart = ({ portfolio, chartOptions }) => {

  const [dataOne, setDataOne] = useState([]);
  const [dataTwo, setDataTwo] = useState([]);


  const chartOptionsBis = {
    
    series: [
      {
        data: dataOne,
        dataGrouping: {
          enabled: false
        }
      },
      {
        data: dataTwo,
        dataGrouping: {
          enabled: false
      }
      },
    ],
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8081/test_comparative"
        );
        console.log(response)
        setDataOne(response["data"]["data"]["stock-1"])
        setDataTwo(response["data"]["data"]["stock-2"])
        
        
      
      } catch (error) {
        console.error("Erreur lors de la récupération des données:", error);
      }
    };

    fetchData(); // Appel de la fonction de récupération des données
  }, []);
  console.log("test")
  return (
    <div className="highcharts-dark">
      <HighchartsReact
        highcharts={Highcharts}
        constructorType={"stockChart"}
        options={chartOptionsBis}
      />
    </div>
  );
};

export default StockChart;
