
import unittest
import os
import shutil
import tempfile
from repo_depth_analyser.src.scanner import Scanner

class TestDotNetPatterns(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)
        
    def create_file(self, filename, content):
        filepath = os.path.join(self.test_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath

    def test_server_side_patterns(self):
        # 1. API Controller (.cs)
        self.create_file('Controllers/ApiController.cs', '''
        using System.Web.Http;
        [ApiController]
        [Route("api/users")]
        public class UsersController : ApiController {
            [HttpGet]
            public IHttpActionResult GetUsers() { }
        }
        ''')

        # 2. WebMethod (.aspx.cs)
        self.create_file('Pages/Default.aspx.cs', '''
        public partial class Default : System.Web.UI.Page {
            [WebMethod]
            public static string GetData() { return "data"; }
            
            protected void Page_Load(object sender, EventArgs e) {
                ScriptManager.RegisterStartupScript(this, GetType(), "alert", "alert('hi');", true);
            }
        }
        ''')

        # 3. Razor View (.cshtml)
        self.create_file('Views/Home/Index.cshtml', '''
        @Ajax.ActionLink("Load", "Get", new AjaxOptions { UpdateTargetId = "div1" })
        <script>
            var url = '@Url.Action("GetData", "Home")';
            fetch(url);
        </script>
        ''')
        
        # 4. Web.config
        self.create_file('Web.config', '''
        <configuration>
            <system.web.extensions>
                <scripting>
                    <scriptResourceHandler enableCompression="true" enableCaching="true" />
                </scripting>
            </system.web.extensions>
        </configuration>
        ''')
        
        # 5. Third Party (.aspx)
        self.create_file('Pages/Grid.aspx', '''
        <telerik:RadAjaxManager ID="RadAjaxManager1" runat="server">
        </telerik:RadAjaxManager>
        <dx:ASPxCallbackPanel ID="CallbackPanel" runat="server">
        </dx:ASPxCallbackPanel>
        ''')

        scanner = Scanner(self.test_dir)
        inventory, stats, ajax_details = scanner.scan()
        
        # Helper to find matches
        def find_matches(filename, pattern_snippet):
            return [d for d in ajax_details if d['Filename'] == filename and pattern_snippet.lower() in d['Code_Snippet'].lower()]

        # Assertions
        
        # Check API Controller
        api_matches = find_matches('ApiController.cs', '[ApiController]')
        self.assertTrue(api_matches, "Should detect [ApiController]")
        self.assertEqual(api_matches[0]['Category'], "Server")
        self.assertEqual(api_matches[0]['Capability'], "API Endpoint (Server)")

        # Check WebMethod
        webmethod_matches = find_matches('Default.aspx.cs', '[WebMethod]')
        self.assertTrue(webmethod_matches, "Should detect [WebMethod]")
        self.assertEqual(webmethod_matches[0]['Category'], "Server")
        
        # Check ScriptManager
        sm_matches = find_matches('Default.aspx.cs', 'ScriptManager.RegisterStartupScript')
        self.assertTrue(sm_matches, "Should detect ScriptManager")
        self.assertEqual(sm_matches[0]['Capability'], "Server-Side Script Injection")

        # Check Razor
        razor_matches = find_matches('Index.cshtml', '@Ajax.ActionLink')
        self.assertTrue(razor_matches, "Should detect @Ajax.ActionLink")
        self.assertEqual(razor_matches[0]['Category'], "Request")
        
        # Check Web.config
        config_matches = find_matches('Web.config', '<system.web.extensions>')
        self.assertTrue(config_matches, "Should detect Web.config patterns")
        self.assertEqual(config_matches[0]['Category'], "Config")
        
        # Check Telerik
        telerik_matches = find_matches('Grid.aspx', 'telerik:RadAjaxManager')
        self.assertTrue(telerik_matches, "Should detect Telerik RadAjaxManager")
        self.assertEqual(telerik_matches[0]['Category'], "Third-Party")

        print("All .NET patterns verified successfully!")

if __name__ == '__main__':
    unittest.main()
