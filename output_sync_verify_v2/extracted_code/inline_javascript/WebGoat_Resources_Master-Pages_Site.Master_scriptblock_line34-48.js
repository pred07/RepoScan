$.fx.speeds._default = 500;
			$(function() {
				$( "#dialog" ).dialog({
					autoOpen: false,
					show: "blind",
					hide: "explode"
				});

				$( "#dialog_link" ).click(function() {
					$( "#dialog" ).dialog( "open" );
						return false;
				});
				
				
			});