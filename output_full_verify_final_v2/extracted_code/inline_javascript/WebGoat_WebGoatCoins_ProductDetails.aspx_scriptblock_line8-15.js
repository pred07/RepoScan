$(document).ready(function () {
            $("div.success").hide();
            setTimeout(function () {
                $("div.success").fadeIn("slow", function () {
                    $("div.success").show();
                });
            }, 500);
        });