import React, { useState, useMemo } from "react";
import AgGridComp from "../components/shared/AgGridComp";
import { saleValueFormatter } from "../components/shared/utils";
import { Card, CardContent, Typography, Grid } from "@mui/material";
import {StockChart} from "../components/shared/StockChart"


export const CryptoPortfolio = () => {
  // Sample data for cryptocurrencies
  const [portfolio, setPortfolio] = useState([]);

  const columnsDefs = [
    {
      headerName: "Exchange",
      field: "exchange",
      rowGroup: true, 
      hide: true
    },
    { headerName: "Asset", field: "asset"},
    {
      headerName: "Amount USD",
      field: "amount_usd",
      filter: "agNumberColumnFilter",
      aggFunc: 'sum',
      valueFormatter: saleValueFormatter,
    },
    {
      headerName: "Quantity",
      field: "quantity",
      filter: "agNumberColumnFilter"
    },
  ];

  const autoGroupColumnDef = useMemo(() => {
    return {
      minWidth: 200,
    };
  }, []);

  const chartOptions = {
    chart: {
      type: 'pie',
    },
    title: {
      text: 'Portfolio Distribution',
    },
    series: [
      {
        name: 'Assets',
        data: portfolio,
      },
    ],
  }

  const updateRowData = ({ rowData, portfolio }) => {
    if (checkIfPorfolioChange(rowData, portfolio)) {
      setPortfolio([...portfolio]);
    } else {
      console.log("no change");
    }
  };

  const checkIfPorfolioChange = (rowData, portfolio) => {
    if (portfolio && rowData) {
      if (portfolio.length == portfolio.length) {
        const isChanges = portfolio.map((ele) => {
          const oldPortfolio = rowData.filter((el) => el.asset == ele.asset);
          if (oldPortfolio && ele) {
            return oldPortfolio.quantity != ele.quantity;
          }
          return oldPortfolio;
        });
        return isChanges.some((bool) => bool === true);
      } else {
        return true;
      }
    } else {
      return true;
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          My portfolio
        </Typography>
        <div className="row">
          <div className="col-6">
          <h2>Aggrid</h2>
          <AgGridComp
            columnDefs={columnsDefs}
            rowData={portfolio}
            updateRowData={(e) => updateRowData(e)}
          />
          </div>
          <div className="col-6">
          <h2>Highchart</h2>
          <StockChart 
          data={portfolio}
          chartOptions={chartOptions}
          />
          </div>
          </div>
        
      </CardContent>
    </Card>
  );
};

export default CryptoPortfolio;
