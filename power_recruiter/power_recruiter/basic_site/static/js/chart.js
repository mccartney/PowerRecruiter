window.onload = function () {
	var chart = new CanvasJS.Chart("chartContainer",
	{
		title:{
			text: "Candidates Chart"
		},
		legend:{
			verticalAlign: "bottom",
			horizontalAlign: "center"
		},
		data: [
		{
			indexLabelFontSize: 20,
			indexLabelFontFamily: "Monospace",
			indexLabelFontColor: "darkgrey",
			indexLabelLineColor: "darkgrey",
			indexLabelPlacement: "outside",
			type: "pie",
			showInLegend: true,
			toolTipContent: "{y} - <strong>#percent%</strong>",
			dataPoints: [
				{  y: 4181563, legendText:"Newly Created", indexLabel: "Newly Created" },
				{  y: 2175498, legendText:"In progress", indexLabel: "In Progress" },
				{  y: 3125844, legendText:"Rejected",exploded: true, indexLabel: "Rejected" },
				{  y: 1176121, legendText:"Hired" , indexLabel: "Hired"},
				{  y: 4303364, legendText:"Contacted" , indexLabel: "Contacted"}
			]
		}
		]
	});
	chart.render();
}