

var buttons = document.getElementsByTagName("button");
var buttonsCount = buttons.length;



for (var i = 0; i <= buttonsCount; i += 1) {
    buttons[i].onclick = function(e) {
       
		if (document.getElementById(this.id).innerHTML == 'Add to cart')
			{

			document.getElementById(this.id).innerHTML = 'Added to cart';
			
			var product_id = document.getElementById(this.id).id;

			$.ajax({
            type: "GET",
            url: "/add_to_cart/",
            data: {
                'product_id' : product_id,
            },
			success: searchSuccess2,
            dataType: 'html',
			
			});
			
			
			}
			
		else if(document.getElementById(this.id).innerHTML == 'Added to cart')
			{
				document.getElementById(this.id).innerHTML = 'Add to cart';
				
			var product_id = document.getElementById(this.id).id;

			$.ajax({
            type: "GET",
            url: "/remove_from_cart_js/",
            data: {
                'product_id' : product_id,
            },
			success: searchSuccess2,
            dataType: 'html',
			
			});
				
			}
    };
}

function searchSuccess2(data, textStatus, jqXHR)
{	

$('#dropdownzz').html(data)
}









