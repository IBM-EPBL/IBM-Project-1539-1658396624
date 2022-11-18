var barChartOptions = {
    series: [{
    data: [10,8,6,4,2]
  }],
    chart: {
    type: 'bar',
    height: 350,
    toolbar:{
        show:false
    },
  },
  colors:[
    "#246dec",
    "#cc3c43",
    "#367952",
    "#f5b74f",
    "#4f35a1"
],
  plotOptions: {
    bar: {
        distributed:true,
      borderRadius: 4,
      horizontal: false,
      columnWidth:'40%'
    }
  },
  dataLabels: {
    enabled: false
  },
  legend:{
    show:false
  },
  xaxis: {
    categories: ["Laptop","Phone","Monitor","Headphones","camera"],
  },
  yaxis:{
    title:{
        text:"Count"
    }
  }
  };

  var barchart = new ApexCharts(document.querySelector("#bar-chart"), barChartOptions);
  barchart.render();