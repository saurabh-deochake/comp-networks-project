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
    		$("#portfolio h4.section-subheading").text($("#search > input").val());
    		$("#event_tab").css("display","block");
    		$("#portfolio").css("display","block");
    		$('#event_tab').click();
    		//click on the function below, so you can get the information
    		//loading

    	}	
    });

    /*
		Once an event is clicked, all the friends would be populated
    */
    var event_friends = function(location){

    }

    /*
		Once an event is clicked, all the other events would be populated
    */
    var other_event = function(location){
    	
    }
})(jQuery); // End of use strict