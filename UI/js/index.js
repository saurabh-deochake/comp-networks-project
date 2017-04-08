$('.form').find('input, textarea').on('keyup blur focus', function (e) {
  
  var $this = $(this),
      label = $this.prev('label');

	  if (e.type === 'keyup') {
			if ($this.val() === '') {
          label.removeClass('active highlight');
        } else {
          label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight'); 
			} else {
		    label.removeClass('highlight');   
			}   
    } else if (e.type === 'focus') {
      
      if( $this.val() === '' ) {
    		label.removeClass('highlight'); 
			} 
      else if( $this.val() !== '' ) {
		    label.addClass('highlight');
			}
    }

});

$('.tab a').on('click', function (e) {
  
  e.preventDefault();
  
  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');
  
  target = $(this).attr('href');

  $('.tab-content > div').not(target).hide();
  
  $(target).fadeIn(600);
  
});

    //login 
    var users = [{
        Name:'Risham Chokshi',
        userName: 'risham33',
        password: 'radhudi',
        instagram: 'risham33',
        facebook: 'sweetrishrocks@yahoo.com',
        twitter: 'risham33'
    }, {
        Name:'Saurabh Deochake',
        userName: 'saurabh.d04',
        password: 'password',
        instagram: 'saurabh.d04',
        facebook: 'saurabh.deochake@yahoo.com',
        twitter: 'saurabh.d04'
    }];

$('.open_search').on('click',function (e){
  //document.location.href = "./search.html";
  //console.log(this.parentNode.parentNode.id === 'signup');
  var goToSearchPage = true;
  var userdata = [];
  if(this.parentNode.parentNode.id === 'signup'){
    $('#signup').find('div.field-wrap>input').each(function(){
      console.log($(this).text() === '');
      console.log($(this).hasClass("check_req"));
      if($(this).text() === '' && $(this).hasClass("check_req")){
        goToSearchPage = false;
      } 
      //try to add this field in there    
    });
    if(goToSearchPage === true){
      console.log("here");
      //add it to the datastructure
      users.push({Name: $("#firstName").text() + $("#lastName").text(), userName: $("#userName").text(), password: $("#Password").text(), instagram: $("#InstaUsername").text(), facebook: $("#FBUsername").text(),twitter: $("#TwitUsername").text()});
      //send it through the API. 
    }
  }
   else {
    if(this.parentNode.parentNode.id === 'login'){
    $('#login').find('div.field-wrap>input').each(function(){
      if($(this).text() === '' && $(this).hasClass("check_req")){
        goToSearchPage = false;
        console.log(false);
      }
      //try to add this field in there    
    });
    console.log("all good");
    if(goToSearchPage === true){
      //send an api
      var result = $.grep(users, function(e){ return e.userName == $("#loginUser").text(); });
      if (result.length >= 1) {
        //send the item using result[0].userName ... 
      }
    }
    
  }
}
});