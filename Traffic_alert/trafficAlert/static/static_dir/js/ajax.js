
$(function() {
	
    $('#search').keyup(function() {

        $.ajax({
            type: "GET",
            url: "/search_area_func/",
            data: {
                'search_area' : $('#search').val(),
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });


	
});

function searchSuccess(data, textStatus, jqXHR)
{	
    $('#search-resultsss').html(data)

}