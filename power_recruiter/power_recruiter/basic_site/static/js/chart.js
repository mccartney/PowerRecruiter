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
				{  y: 4181563, legendText:"PS 3", indexLabel: "" },
				{  y: 2175498, legendText:"Wii", indexLabel: "Wii" },
				{  y: 3125844, legendText:"360",exploded: true, indexLabel: "Xbox 360" },
				{  y: 1176121, legendText:"DS" , indexLabel: "Nintendo DS"},
				{  y: 1727161, legendText:"PSP", indexLabel: "PSP" },
				{  y: 4303364, legendText:"3DS" , indexLabel: "Nintendo 3DS"},
				{  y: 1717786, legendText:"Vita" , indexLabel: "PS Vita"}
			]
		}
		]
	});
	chart.render();
}