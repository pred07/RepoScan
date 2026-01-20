// 1. Obfuscated / Dynamic Execution
        // Static analysis often misses eval() content unless specifically looking for it
        var code = "console.log('Secret code executed via eval()')";
        eval(code);

        // 2. Dynamic Script Injection
        // The crawler SHOULD catch this if it executes
        var s = document.createElement('script');
        s.src = "https://example.com/analytics.js"; // External resource
        document.head.appendChild(s);

        // 3. Dynamic Style Injection
        var css = "body { background-color: #333; color: #fff; }";
        var style = document.createElement('style');
        style.type = 'text/css';
        if (style.styleSheet) {
            style.styleSheet.cssText = css;
        } else {
            style.appendChild(document.createTextNode(css));
        }
        document.head.appendChild(style);

        // 4. Base64 Encoded Execution (Very hard for regex)
        var encoded = "YWxlcnQoJ0lzIHRoaXMgZGV0ZWN0ZWQ/Jyk7"; // alert('Is this detected?');
        var decoded = atob(encoded);
        // Function constructor execution
        new Function(decoded)();