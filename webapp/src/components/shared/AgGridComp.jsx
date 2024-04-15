import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';

import { RowGroupingModule } from '@ag-grid-enterprise/row-grouping';
import { ServerSideRowModelModule } from '@ag-grid-enterprise/server-side-row-model';
import { LicenseManager } from '@ag-grid-enterprise/core';
LicenseManager.setLicenseKey("my-license-key");

import { AgGridReact } from 'ag-grid-react';
import React, { useEffect, useMemo } from "react";
import axios from "axios";

const AgGridComp = ({ columnDefs, rowData, updateRowData, autoGroupColumnDef }) => {
  const gridOptions = {
    columnDefs: columnDefs,
    defaultColDef: {
      editable: true,
      flex: 1,
      minWidth: 100,
    },
    rowData: rowData,

  };

  const defaultColDef = useMemo(() => {
    return {
      flex: 1,
      minWidth: 150,
    };
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8081/get_portfolio_data"
        );
        updateRowData({
          rowData: rowData,
          portfolio: response.data.portfolio,
        }); // Assurez-vous que la structure des données correspond à vos besoins
      } catch (error) {
        console.error("Erreur lors de la récupération des données:", error);
      }
    };

    fetchData(); // Appel de la fonction de récupération des données
  }, []); // Le tableau vide en tant que deuxième argument signifie que cela ne s'exécutera qu'une seule fois au montage


  const getRowData = () => {
    return rowData.filter((x) => {
      if (x.amount_usd > 0.00001) {
        return x;
      }
    });
  };

  return (
    <>
      <div>
        <div
          className="ag-theme-quartz-dark"
          style={{ height: "400px", width: "100%" }}
        >
          <AgGridReact
            gridOptions={gridOptions}
            defaultColDef={defaultColDef}
            modules={[RowGroupingModule, ServerSideRowModelModule]}
            rowData={getRowData()}
          />
        </div>
      </div>
    </>
  );
};

export default AgGridComp;
