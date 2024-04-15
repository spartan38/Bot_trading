import React, { useEffect, useRef } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

const PieChart = ({ data, chartOptions }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (chartRef.current) {
      // Create the chart
      const chart = Highcharts.chart(chartRef.current, chartOptions);

      // Cleanup on component unmount
      return () => {
        chart.destroy();
      };
    }
  }, [data]);

  return <div ref={chartRef} />;
};

export default PieChart;