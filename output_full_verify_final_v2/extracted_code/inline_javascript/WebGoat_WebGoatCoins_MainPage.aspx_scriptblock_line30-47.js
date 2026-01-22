$(document).ready(function() {
            var admin = <%= (User.IsInRole("admin") ? 1 : 0 ) %>;  
            if(admin == 0) //not an admin
            { 
                $("#ctl00_BodyContentPlaceholder_logoFileName").hide();
                $("#ctl00_BodyContentPlaceholder_question_id").hide();
                $("#ctl00_BodyContentPlaceholder_password").hide();
                $("#ctl00_BodyContentPlaceholder_answer").hide();
            }
                    
            $("div.success").hide();
                    
            setTimeout(function () {
                $("div.success").fadeIn("slow", function () {
                    $("div.success").show();
                });
            }, 500);
        });