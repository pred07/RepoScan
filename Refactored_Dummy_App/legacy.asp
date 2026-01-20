<%@ Language="VBScript" %>
    <!DOCTYPE html>
    <html>

    <head>
        <title>Legacy Page (Do Not Refactor)</title>
        <style>
            .error {
                color: red;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <h1>Old Reports System</h1>

        <% Dim userName userName="AdminUser" Response.Write("<h2>Welcome back, " & userName & "</h2>")
            %>

            <script type="text/javascript">
                // This script block interacts with server-side variable
                var currentUser = "<%= userName %>";

                if (currentUser === "") {
                    alert("No user logged in.");
                } else {
                    console.log("Logged in as: " + currentUser);
                }

                function validateForm() {
                    // Legacy validation
                    if (document.forms[0].reportDate.value == "") {
                        alert("Date is required.");
                        return false;
                    }
                    return true;
                }
            </script>

            <form onsubmit="return validateForm()">
                <input type="text" name="reportDate" />
                <input type="submit" value="Generate" />
            </form>

    </body>

    </html>