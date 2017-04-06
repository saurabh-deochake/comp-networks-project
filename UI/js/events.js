(function($) {
    "use strict"; // Start of use strict

    /*
		This is function for whatever is entered in the text box,
		it will spin out information about that location
    */
    $('#search > a').on("click",function(){
    	//check for the empty value
    	if($("#search > input").val() == ""){
    		alert("Please put a value in input box");
    	} else {
    		var location = $("#search > input").val(); 
    		$("#portfolio h4.section-subheading").text(location);
    		$("#event_tab").css("display","block");
    		$("#portfolio").css("display","block");
            $("#popularity").css("display","block");

    		$('#event_tab').click();
    		//click on the function below, so you can get the information
    		//loading
    		
            //heatmap
            Highcharts.chart('heatmap', {
                chart: {
                    backgroundColor: "#EEE"
                },
                colorAxis: {
                    minColor: '#FFFFFF',
                    maxColor: Highcharts.getOptions().colors[8]
                },
                series: [{
                    type: 'treemap',
                    layoutAlgorithm: 'squarified',
                    data: [{
                        name: 'A',
                        value: 6,
                        colorValue: 1
                    }, {
                        name: 'B',
                        value: 6,
                        colorValue: 2
                    }, {
                        name: 'C',
                        value: 4,
                        colorValue: 3
                    }, {
                        name: 'D',
                        value: 3,
                        colorValue: 4
                    }, {
                        name: 'E',
                        value: 2,
                        colorValue: 5
                    }, {
                        name: 'F',
                        value: 2,
                        colorValue: 6
                    }, {
                        name: 'G',
                        value: 1,
                        colorValue: 7
                    }]
                }],
                title: {
                    text: ''
                }
            });

            event_friends(location);
    		other_event(location);
    	}	
    });

    /*
		Once an event is clicked, all the friends would be populated
    */
    var event_friends = function(location){
    	var arrival = "2:00PM";
    	var departure = "3:00PM";
    	var image = "img/team/3_.jpg"
    	var event_name = "Barbeque";
    	var person_name = "Gary Johnson";
    	var event_start = "2:00PM";
    	var event_end = "6:00PM";
    	var event_address = "252 Hamilton St, New Brunswick, NJ";
    	
    	$('#portfolioModal1 .modal-body > div.row').text("");

		$('#portfolioModal1 .modal-body>div.row').append('<div class="col-md-4 col-sm-6 col-lg-4"><div class="panel panel-default"> <div class="panel-heading"><h4 style="margin-top: 0px;margin-bottom: 0px;">'+person_name+'</h4><br><strong>Arrived:</strong>'+arrival+'<br><strong>Till: </strong>'+departure+'</div> <div class="panel-body"><img class="img-circle img-responsive" src="'+image+'" alt="" align="middle"><div class="panel-heading"><h5 style="margin-top: 0px;margin-bottom: 0px;">'+event_name+'</h5><br><strong>Location</strong>: '+event_address+' <br><strong>Starting Time</strong>: '+event_start+'<br><strong>Ending Time</strong>: '+event_end+'</div></div></div></div>');

    	//started from the top
    	arrival = "5:00PM";
    	departure = "6:00PM";
    	image = "img/team/1.jpg";
    	event_name = "Bowling";
    	person_name = "Bob Johnson";
    	event_start = "3:00PM";
    	event_end = "6:00PM";
    	event_address = "12 Scott Hall, New Brunswick, NJ";
		$('#portfolioModal1 .modal-body>div.row').append('<div class="col-md-4 col-sm-6 col-lg-4"><div class="panel panel-default"> <div class="panel-heading"><h4 style="margin-top: 0px;margin-bottom: 0px;">'+person_name+'</h4><br><strong>Arrived:</strong>'+arrival+'<br><strong>Till: </strong>'+departure+'</div> <div class="panel-body"><img class="img-circle img-responsive" src="'+image+'" alt="" align="middle"><div class="panel-heading"><h5 style="margin-top: 0px;margin-bottom: 0px;">'+event_name+'</h5><br><strong>Location</strong>: '+event_address+' <br><strong>Starting Time</strong>: '+event_start+'<br><strong>Ending Time</strong>: '+event_end+'</div></div></div></div>');
    };

    /*
		Once an event is clicked, all the other events would be populated
    */
    var other_event = function(location){
    	$('#portfolioModal2 .modal-body>div.row').text("");
    	var event_name = "Hackthon";
    	var event_address = "Cook Campus Center"; 
    	var event_start = "Saturday, May 31 12:00PM";
    	var event_end = "Sunday, June 1 12:00PM";
    	$('#portfolioModal2 .modal-body>div.row').append('<div class="col-md-4 col-sm-6 col-lg-4"><div class="panel panel-default"> <div class="panel-heading">'+event_name+'</div> <div class="panel-body"><strong>Location</strong>: '+event_address+' <br><strong>Start Time</strong>: '+event_start+'<br><strong>End Time</strong>: '+event_end+'</div></div></div>');
    };


    
})(jQuery); // End of use strict

