// Native Fetch
        fetch('/api/data');

        // XHR
        var xhr = new XMLHttpRequest();
        xhr.open("GET", '/api/old');

        // JQuery
        $.ajax({ url: '/test' });
        $.get('/test');
        $.post('/test');

        // Axios
        axios.get('/api/axios');

        // Websocket
        new WebSocket('ws://localhost');