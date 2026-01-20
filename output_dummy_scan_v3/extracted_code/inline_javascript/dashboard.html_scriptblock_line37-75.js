// Complex Inline Script with AJAX
        $(document).ready(function () {
            console.log("Dashboard initialized.");

            // 1. AJAX Call (Detectable)
            function loadStats() {
                $.ajax({
                    url: "/api/stats",
                    method: "GET",
                    success: function (data) {
                        $("#user-stats").html("<strong>Users:</strong> " + data.users);
                    },
                    error: function () {
                        $("#user-stats").text("Failed to load stats.");
                    }
                });
            }

            // 2. Fetch API (Detectable)
            fetch('/api/notifications')
                .then(response => response.json())
                .then(data => {
                    const list = data.map(n => `<li>${n}</li>`).join('');
                    document.getElementById('notifications').innerHTML = `<ul>${list}</ul>`;
                });

            // 3. jQuery Event Handler
            $("#refresh-btn").click(function () {
                alert("Refreshing...");
                loadStats();
            });

            // Initial Load
            loadStats();
        });

        // CSP Violation Test
        // This variable assignment might be tricky for regex-based static analysis
        var cspHeader = "default-src 'self'; script-src 'unsafe-inline'";