// Dynamic Script
        var scriptEl = document.createElement('script');
        scriptEl.src = 'dynamic.js';
        document.body.appendChild(scriptEl);

        // Eval & Friends
        eval('console.log("danger")');
        new Function('return true');
        setTimeout(() => { }, 1000);
        setInterval(() => { }, 1000);

        // InnerHTML Sink
        document.body.innerHTML = '<div>New Content</div>';