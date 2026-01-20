// Simple inline script
        console.log("Index page loaded.");

        function updateTime() {
            const now = new Date();
            document.title = "Dummy App - " + now.toLocaleTimeString();
        }

        setInterval(updateTime, 1000);