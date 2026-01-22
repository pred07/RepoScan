// Dynamic Style/Link
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'dynamic.css';

        // Direct Style Manipulation
        document.body.style.color = 'blue';
        document.body.style['backgroundColor'] = 'white';

        // CSSOM
        document.body.style.setProperty('margin', '10px');

        // Constructible Stylesheets
        const sheet = new CSSStyleSheet();
        document.adoptedStyleSheets = [sheet];