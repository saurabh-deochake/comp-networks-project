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

$('.open_search').on('click',function (e){
  document.location.href = "./search.html";
  //console.log(this.parentNode.parentNode.id === 'signup');
  /*var goToSearchPage = true;
  if(this.parentNode.parentNode.id === 'signup'){
    $('#signup').find('div.field-wrap>input').each(function(){
      /*console.log($(this).text() === '');
      console.log($(this).hasClass("check_req"));
      if($(this).text() === '' && $(this).hasClass("check_req")){
        goToSearchPage = false;
      }
      //try to add this field in there    
    });
    if(goToSearchPage)
      document.location.href = "./search.html";
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
    //if(goToSearchPage)
      //document.location.href = "./search.html";
  }
}*/
});